if (!process.env.NODE_ENV) {
  console.error('Please set NODE_ENV environment variable');
  process.exit(1)
}

const env = process.env.NODE_ENV
if (env === 'development') {
  require('dotenv').config()  
}

const apiKey = process.env.GPT_API_KEY

if (!apiKey) {
  console.error('Please set GPT_API_KEY environment variable.')
  process.exit(1)
}

const promptStorageDirectory = process.env.PROMPT_STORAGE_DIRECTORY || "~/.janus/prompts"

const config = {
  apiKey,
  promptStorageDirectory,
}

export default config
