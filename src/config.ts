const apiKey = process.env.GPT_API_KEY

if (!apiKey) {
  console.error('Please set GPT_API_KEY environment variable.')
  sys.exit(1)
}

const promptStorageDirectory = process.env.PROMPT_STORAGE_DIRECTORY || "~/.janus/prompts"

const config = {
  apiKey,
  promptStorageDirectory,
}

export default config
