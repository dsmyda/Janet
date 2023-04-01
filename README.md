# Janet

Janet will read your database DLL, do a bit of prompt engineering, and then automatically generate SQL queries that answer your question. Janus is designed to do basic descriptive analytics - which broadly means it'll help you summarize the past and find counts, trends, etc. The intention of this tool is to automate the first step of most data analytics workflows, the development of ad-hoc dashboards for monitoring and visualization, and to reduce the load on teams that get asked analytics questions in Slack. 

Janet currently only supports Postgres. I might expand it to include database engines in the future.

## Components
WIP

### Web Server

#### POST /api/ddl 

Load the database ddl beforehand. Janet will fetch tables matching filters using a read only connection. The ddl will be saved to disk and used on calls to `/api/answer`, if requested. See `/api/answer` for more details.

Request Body

```typescript
{
  name: string, // must be unique 
  filters?: {
    schemas?: string[] // defaults to ['public']
    includeTables: RegExp[], // defaults to ["/*/"]
    excludeTables: RegExp[], // defaults to [] 
  }
}
```

Example
```sh
curl -X POST -H "Content-Type: application/json" -d "{ \"name\": \"public\" }" http://localhost:3000/api/ddl
```

#### POST /api/answer

Answer a basic analytics question. If a `ddl` is not passed, then it'll call `/api/ddl` beforehand. To speed up queries and lower usage costs, it's recommened you create prompts beforehand, and to only include the minimal number of required DDLs to answer the question.

Request body

```typescript
{
  question: string,
  ddlName?: string, // makes a default call to /api/ddl, but doesn't persist the result.
  runQuery?: boolean, // defaults to true 
  gptParams?: Record<string, any> // these values will be passed verbatim to GPT 
}
```

Example

```sh
curl -X POST -H "Content-Type: application/json" -d "{ \"ddlName\": \"public\", \"question\": \"How many employees were hired in 2003?\" }" http://localhost:3000/api/answer
```
