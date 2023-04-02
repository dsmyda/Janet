import express from 'express'
import * as preloadApi from '../../src/core/preload'
import * as answerApi from '../../src/core/openai'
import { send200, send400, send500 } from './utils'
import { ZodQuestionPostBody, ZodPreloadPostBody } from './interfaces'
import { queryUntilSuccess } from '../../src/core/query'
import config from '../../src/core/config'

const app = express()
app.use(express.json())
app.use(function(_, res, next) {
  res.header('Content-Type', 'application/json');
  next()
})

app.post('/api/preload', (req, res) => {
  ZodPreloadPostBody.safeParseAsync(req.body)
   .then((parseResult) => {
      if (!parseResult.success) {
        send400(res, parseResult.error)
      } else {
        const safePayload = parseResult.data
        preloadApi.create(safePayload.name, safePayload.filters)
          .then(() => send200(res, 'Prompt created.'))
          .catch((err: any) => {
            console.error(err)
            send500(res)
          })
      } 
    })
})

app.post('/api/question', (req, res) => {
  const parseResult = ZodQuestionPostBody.safeParse(req.body)
  if (!parseResult.success) {
    send400(res, parseResult.error)
    return
  }

  const safePayload = parseResult.data
  answerApi.getCandidateQueries(config.databaseInfo.engine, safePayload.question, safePayload.preloadName)
    .then((queries: string[]) => {
      queryUntilSuccess(queries)
        .then(([results, query]) => {
          send200(res, {
            results: results.data,
            query
          })
        })
        .catch((err: Error) => {
          console.error(err)
          send500(res)
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
