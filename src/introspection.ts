import pgStructure, { Column, Index } from "pg-structure";
import { ConnectionInfo } from './config'
import { Filters } from "./interfaces";

function columnReducer(prev: any, column: Column) {
  const columnKey = `"${column.name}"`
  if (column.type.hasLength) {
    prev[columnKey] = `${column.type.name}(${column.length})`
  } else if (column.type.hasPrecision && column.type.hasScale) {
    prev[columnKey] = `${column.type.name}(${column.precision}, ${column.scale})`
  } else {
    prev[columnKey] = column.type.name
  }

  if (column.foreignKeys.length > 0) {
    prev[columnKey] += ` REFERENCES ${column.foreignKeys[0].referencedTable.fullName}(${column.foreignKeys[0].referencedColumns.map((c) => c.name).join(', ')})`
  }
  
  return prev
}

function indexMapper(index: Index) {
  return {
    name: index.name,
    columns: index.columns.map((column) => column.name),
    unique: index.isUnique,
    primary: index.isPrimaryKey,
    partial: index.isPartial,
  }
}

export async function getDatabaseStructure(engine: string, connectionInfo: ConnectionInfo, filters: Filters) {
  if (engine === 'postgres') {
    const db = await pgStructure(connectionInfo, { includeSchemas: filters.schemas })
    const ret = []
    for (const table of db.tables) {
      ret.push({
        name: `"${table.schema.name}"."${table.name}"`,
        columns: table.columns.reduce(columnReducer, {} as any),
        indexes: table.indexes.map(indexMapper),
      })
    }
    
    return ret
  } else {
    throw new Error('Database engine is not supported')
  }
}
