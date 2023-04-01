export type ConnectionInfo = {
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

checkOrFail(process.env.OPENAI_API_KEY, 'Please set GPT_API_KEY environment variable.')

const engine = process.env.DATABASE_ENGINE || 'postgres'
const database = process.env.DATABASE_NAME || 'postgres'
const host = process.env.DATABASE_HOST || 'localhost'
const user = process.env.DATABASE_USER || 'postgres'
const password = process.env.DATABASE_PASSWORD || 'postgres'
const port = (process.env.DATABASE_PORT) ? Number(process.env.DATABASE_PORT) : 5432 

const openAIApiKey = process.env.OPENAI_API_KEY
const promptStoragePath = process.env.PROMPT_STORAGE_PATH || '~/.janet/prompts'

const config = {
  openAIApiKey,
  engine,
  info: { database, user, host, password, port },
  promptStoragePath
}

export default config
