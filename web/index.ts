import express from 'express'
import * as promptApi from '../src/prompt'
import * as answerApi from '../src/openai'
import { send200, send400, send500 } from './utils'
import { ZodAnswerPostBody, ZodPromptPostBody } from '../src/interfaces'
import { runQuery } from '../src/database'
import config from '../src/config'

const app = express()
app.use(express.json())
app.use(function(_, res, next) {
  res.header('Content-Type', 'application/json');
  next()
})

app.post('/api/ddl', (req, res) => {
  const body = req.body
  const parseResult = ZodPromptPostBody.safeParse(body)
  if (!parseResult.success) {
    send400(res, parseResult.error)
    return
  }

  const safePayload = parseResult.data
  promptApi.exists(safePayload.name)
    .then((exists: boolean) => {
      if (exists) {
        send400(res, `Prompt with name '${safePayload.name}' already exists.`)
      } else {
        promptApi.create(safePayload.name, safePayload.filters)
        .then(() => send200(res, `Prompt with name '${safePayload.name}' created.`))
        .catch((err: Error) => { 
          console.error(err)
          send500(res) 
        })
      } 
    })
  })

app.post('/api/answer', (req, res) => {
  const body = req.body
  const parseResult = ZodAnswerPostBody.safeParse(body)
  if (!parseResult.success) {
    send400(res, parseResult.error)
    return
  }

  const safePayload = parseResult.data
  answerApi.getAnswer(safePayload.question, safePayload.ddlName)
    .then((query: string) => {
      runQuery(config.engine, query)
        .then((results: any) => {
          send200(res, {
            results,
            query
          })
        })
    })
    .catch((err: Error) => {
      console.error(err)
      send500(res)
    })
})

app.listen(3000, () => {
  console.log('Janet is listening on port 3000. Ready to serve web traffic.')
})
