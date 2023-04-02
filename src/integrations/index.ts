import { DatabaseConnectionInfo } from '../core/config'
import { getPostgresClient } from './postgres'

export enum DatabaseEngine {
  Postgres = 'postgres'
}

export type DatabaseResult = {
  data: Record<string, any>[],
}

export type StructureFilters = {
  schemas: string[]
}

export type Entity = {
  name: string,
  columns: Record<string, string>
  indexes: Record<string, string>[]
}

export interface DatabaseClient {
  connect(): Promise<void>
  query(query: string): Promise<DatabaseResult>
  getStructure(filters: StructureFilters): Promise<Entity[]>
  end(): Promise<void>
}

export function getClient(connectionInfo: DatabaseConnectionInfo): DatabaseClient {
  const { engine } = connectionInfo
  if (engine === DatabaseEngine.Postgres) {
    return getPostgresClient(connectionInfo)
  }

  throw new Error(`Database engine ${engine} is not supported`)
}
