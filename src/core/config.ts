export type DatabaseConnectionInfo = {
  engine: string,
  database: string,
  host: string,
  user: string,
  password: string,
  port: number
}

function checkOrFail(variable: any, msg: string) {
  if (!variable) {
    console.error(msg)
    process.exit(1)
  }
}

checkOrFail(process.env.NODE_ENV, 'Please set the NODE_ENV environment variable')

const env = process.env.NODE_ENV
if (env === 'development') {
  require('dotenv').config()
}

checkOrFail(process.env.OPENAI_API_KEY, 'Please set OPENAI_API_KEY environment variable.')

const online = process.env.ONLINE || 'true'
if (online === 'true') {
  checkOrFail(process.env.DATABASE_ENGINE, 'Please set DATABASE_ENGINE environment variable.')
  checkOrFail(process.env.DATABASE_NAME, 'Please set DATABASE_NAME environment variable.')
  checkOrFail(process.env.DATABASE_HOST, 'Please set DATABASE_HOST environment variable.')
  checkOrFail(process.env.DATABASE_USER, 'Please set DATABASE_USER environment variable.')
  checkOrFail(process.env.DATABASE_PASSWORD, 'Please set DATABASE_PASSWORD environment variable.')
  checkOrFail(process.env.DATABASE_PORT, 'Please set DATABASE_PORT environment variable.')
}

const engine = process.env.DATABASE_ENGINE!
const database = process.env.DATABASE_NAME!
const host = process.env.DATABASE_HOST!
const user = process.env.DATABASE_USER!
const password = process.env.DATABASE_PASSWORD!
const port = (process.env.DATABASE_PORT) ? Number(process.env.DATABASE_PORT) : 5432 

const openaiKey = process.env.OPENAI_API_KEY
const preloadStoragePath = process.env.PRELOAD_STORAGE_PATH || '~/.janet/prompts'

const config = {
  online,
  databaseInfo: {
    engine,
    database, 
    user,
    host, 
    password, 
    port
  },
  openaiKey,
  preloadStoragePath
}

export default config
