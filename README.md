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
curl "http://localhost:3000/api/prompt" -D '{ "name": "public", "connectionURL": "..." }'
```

#### POST /api/answer

Answer a basic analytics question. If a promptName is not passed, then it'll call /api/prompt beforehand. To speed up queries and lower usage costs, it's recommened you create prompts beforehand, and to only include
the minimal number of required DDLs to answer the question.

Request body

```typescript
{
  question: string,
  promptName?: string, // makes a default call to /api/prompt, but doesn't persist the result.
  runQuery?: boolean, // defaults to true 
  gptParams: Record<string, any> // these values will be passed verbatim to GPT 
  
}
```

Example

```sh
curl "http://localhost:3000/api/answer" -D '{ "promptName": "public", "question": "How many assignments were created in the last 24 hours for userId 'danny'" }'
```
