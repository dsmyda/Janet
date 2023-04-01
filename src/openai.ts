import axios from 'axios'
import config from './config'
import { getDatabaseStructure } from './introspection'
import * as preloadApi from './preload'

async function getEngineeredPrompt(question: string, ddlName?: string) {
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

Use the PostgreSQL 10+ database below to create a SQL query to answer the question above.
I must wrap table names and column names in double quotes, no exceptions.
    
Postgres Database: """
${databaseSchema}
"""
`
}

export async function getAnswer(question: string, ddlName?: string) {
  const prompt = await getEngineeredPrompt(question, ddlName)

  const { status, data } = await axios.post('https://api.openai.com/v1/completions', {
    model: 'text-davinci-003',
    prompt,
    max_tokens: 500,
  }, {
    headers: {
      'Authorization': `Bearer ${process.env.OPENAI_API_KEY}`,
      'Content-Type': 'application/json'
    }
  })

  if (status !== 200) {
    throw new Error(`OpenAI API returned status code ${status}, data: ${JSON.stringify(data)}`)
  }

  return data.choices[0].text
}
