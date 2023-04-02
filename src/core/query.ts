import config from './config'
import { getClient } from '../integrations'
import axios from 'axios';

export async function queryUntilSuccess(queries: string[]) {
  const client = getClient(config.databaseInfo);
  await client.connect()

  for (const query of queries) {
    try {
      const safeQuery = await transformQuery(query)
      const result = await client.query(safeQuery)
      await client.end()

      return [result, safeQuery]
    } catch (err: any) {
      console.log('Failed to run query', err)
    }
  }

  await client.end()
  
  throw new Error(`No query succeeded`)
}

export async function transformQuery(query: string) {
  const result = await axios.post(`http://localhost:5000/transform`, {
    query,
  })
  
  const { transformed } = result.data
  return transformed
}