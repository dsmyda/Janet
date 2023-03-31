import express from 'express'
import config from '@/config'

const app = express()

app.post('/api/prompt', (req, res) => {
  res.send('Hello word')
})

app.listen(3000, () => {
  console.log('Janus is listening on port 3000. Ready to serve web traffic.')
})
