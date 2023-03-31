import express from 'express'
import config from '../src/config'

const app = express()

app.post('/api/prompt', (req, res) => {
  res.send('Hello, prompt')
})

app.post('api/answer', (req, res) => {
  res.end('Hello, answer');
})

app.listen(3000, () => {
  console.log('Janus is listening on port 3000. Ready to serve web traffic.')
})
