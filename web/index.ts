import express from 'express'
import * as promptApi from '../src/prompt'
import { send200, send400, send500 } from './utls'
import { ZodPromptPostBody } from '../src/interfaces'

const app = express()
app.use(express.json())
app.use(function(_, res, next) {
  res.header('Content-Type', 'application/json');
  next()
})

app.post('/api/prompt', (req, res) => {
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

app.post('api/answer', (req, res) => {
  res.end('Hello, answer');
})

app.listen(3000, () => {
  console.log('Janet is listening on port 3000. Ready to serve web traffic.')
})
