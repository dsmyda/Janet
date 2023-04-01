import { Client } from 'pg'
import config from './config'

function getClient(engine: string) {
  const { user, password, host, port, database } = config.info

  if (engine === 'postgres') {
    const client = new Client({
      user,
      password,
      host,
      port,
      database,
    })

    return client
  }

  throw new Error('Database engine is not supported')
}

export async function runQuery(engine: string, sql: string) {
  const client = getClient(engine);
  await client.connect()

  const result = await client.query(sql)

  const { rows } = result
  const formattedRows = rows.map((row) => {
    const formattedRow: Record<string, any> = {}
    for (const key in row) {
      formattedRow[key] = row[key]
    }
    return formattedRow
  })

  await client.end()

  return formattedRows
}
