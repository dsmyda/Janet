# Janus

Janus will read your database DLL, do a bit of prompt engineering, and then automatically generate SQL queries that answer your question. Janus is designed to do basic descriptive analytics - which broadly means it'll help you summarize the past and find counts, trends, etc. The intention of this tool is to automate the first step of most data analytics workflows, the development of ad-hoc dashboards for monitoring and visualization, and to reduce the load on teams that get asked analytics questions in Slack. 

## Components
WIP

### Web Server

#### POST /api/prompt 

Create a prompt. Janus will fetch tables matching filters using a read only connection. The prompt will be saved to disk and attached on each request sent to `/api/answer`, if requested.

Request Body

```typescript
{
  name: string, // must be unique 
  filters?: {
    schema?: string // defaults to public
    includeTables: RegExp[], // defaults to ["/*/"]
    excludeTables: RegExp[], // defaults to [] 
  }
}
```

Example

```sh
curl "http://localhost:3000/api/prompt" -D '{ "name": "test-prompt", "connectionURL": "..." }'
```

#### POST /api/answer

Request body

```typescript
{
  prompt: string,
  question: string,
  runQuery?: boolean, // defaults to true 
  gptParams: Record<string, any> // these values will be passed verbatim to GPT 
  
}
```

Example

```sh
curl "http://localhost:3000/api/answer" -D '{ "prompt": "public", "question": "How many assignments were created in the last 24 hours for userId 'danny'" }'
```
