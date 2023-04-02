import config from './config'
import { writeFile, stat, mkdir, readFile } from 'fs/promises'
import { StructureFilters } from '../integrations'
import { Entity, getClient } from '../integrations'

function getPreloadPath(name: string) {
  return `${config.preloadStoragePath}/${name}.json`
}

export async function exists(name: string) {
  try {
    await stat(getPreloadPath(name))
    return true
  } catch (err) {
    return false
  }
}

async function save(name: string, data: Entity[]) {
  await mkdir(config.preloadStoragePath, { recursive: true })
  await writeFile(getPreloadPath(name), JSON.stringify(data), { encoding: 'utf-8', flag: 'w' })
}

export async function create(name: string, filters: StructureFilters) {
  if (await exists(name)) {
    throw new Error(`Preload with name '${name}' already exists.`)
  } else {
    const client = getClient(config.databaseInfo)

    const data = await client.getStructure(filters)
    await save(name, data)
  }
}

export async function load(name: string) {
  if (await exists(name)) {
    return await readFile(getPreloadPath(name), { encoding: 'utf-8' })
  } else {
    throw new Error(`Preload with name '${name}' does not exist.`)
  }
}
