import axios from 'axios'
import * as preloadApi from './preload'

const DEFAULT_PARAMS = {
  model: 'text-davinci-003',
  temperature: 1,
  n: 3,
  max_tokens: 150
}

async function getEngineeredPrompt(engine: string, question: string, ddlName?: string) {
  if (!question.endsWith('.')) {
    question += '.' 
  }
  let databaseSchema = ''
  if (ddlName) {
    databaseSchema = await preloadApi.load(ddlName)
  } else {
    // databaseSchema = JSON.stringify(await getDatabaseStructure(config.engine, config.info, { schemas: ['public'], includeTables: ['*'], excludeTables: [] }))
  }

  return `${question}

Use the ${engine} database below to create a SQL query to answer the question above. You must only return the SQL statement, do not include any additional text.
Use the indexes to make your query as efficient as possible.
    
${engine} database: """
${databaseSchema}
"""
`
}

export async function getCandidateQueries(engine: string, question: string, ddlName?: string, params: Record<string, any> = DEFAULT_PARAMS) {
  const prompt = await getEngineeredPrompt(engine, question, ddlName)

  const { status, data } = await axios.post('https://api.openai.com/v1/completions', {
    ...params,
    prompt,
  }, {
    timeout: 5000,
    headers: {
      'Authorization': `Bearer ${process.env.OPENAI_API_KEY}`,
      'Content-Type': 'application/json'
    }
  })

  if (status !== 200) {
    throw new Error(`OpenAI API returned status code ${status}, data: ${JSON.stringify(data)}`)
  }

  console.log('OpenAI API returned', data)
  
  return data.choices.map((data: any) => data.text)
}
