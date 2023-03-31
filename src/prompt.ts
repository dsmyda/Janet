import config from './config'
import { writeFile, stat } from 'fs/promises'
import { Filters } from './interfaces'
import { getDatabaseStructure } from './introspection'

export async function exists(name: string) {
  try {
    await stat(`${config.promptStoragePath}/${name}.json`)
    return true
  } catch (err) {
    return false
  }
}

async function save(name: string, data: Record<string, any>[]) {
  await writeFile(`${config.promptStoragePath}/${name}.json`, JSON.stringify(data), { encoding: 'utf-8', flag: 'w' })
}

export async function create(name: string, filters: Filters) {
  if (await exists(name)) {
    throw new Error(`Prompt with name '${name}' already exists.`)
  } else {
    const data = await getDatabaseStructure(config.engine, config.info, filters)
    await save(name, data)
  }
}

async function load(name: string) {
  if (await exists(name)) {
    return import(`${config.promptStoragePath}/${name}.json`)
  } else {
    throw new Error(`Prompt with name '${name}' does not exist.`)
  }
}