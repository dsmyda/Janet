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

checkOrFail(process.env.GPT_API_KEY, 'Please set GPT_API_KEY environment variable.')
checkOrFail(process.env.READ_ONLY_CONNECTION_URI, 'Please set READ_ONLY_CONNECTION_URI environment variable.')

const readOnlyConnection = process.env.READ_ONLY_CONNECTION_URI
const apiKey = process.env.GPT_API_KEY
const promptStorageDirectory = process.env.PROMPT_STORAGE_DIRECTORY || "~/.janus/prompts"

const config = {
  apiKey,
  readOnlyConnection,
  promptStorageDirectory,
}

export default config
