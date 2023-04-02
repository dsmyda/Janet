import { DatabaseConnectionInfo } from '@/core/config'
import { Client } from 'pg'
import type { DatabaseClient, DatabaseResult, Entity, StructureFilters } from '..'
import { getDatabaseStructure } from './introspection'

export function getPostgresClient(params: DatabaseConnectionInfo): DatabaseClient {
  const { engine, ...other } = params
  const pgClient = new Client({
    user: other.user,
    host: other.host,
    database: other.database,
    password: other.password,
    port: other.port,
  })

  return {
    connect: () => pgClient.connect(),
    end: () => pgClient.end(),
    getStructure: async (filters: StructureFilters): Promise<Entity[]> => getDatabaseStructure(other, filters),
    query: async (query: string): Promise<DatabaseResult> => {
      console.log('Running query', query)
      const data = await pgClient.query(query)
      const { rows } = data
      console.log('Query result', rows)
      return { 
        data: rows.map((row: any) => {
          const onlyAttributes: Record<string, any> = {}
          for (const key in row) {
            onlyAttributes[key] = row[key]
          }

          return onlyAttributes 
        }) 
      }
    },
  }
}
