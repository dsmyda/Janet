# Janet

Janet is capable of indexing your database schema, automatically generating SQL queries with the help of OpenAI and then automatically executing those results against your database.
Only the Table DDL will be shared with OpenAI's API, Janet will never query for or include any row data from your table.

Janet is designed to do basic descriptive analytics - which broadly means it'll help you summarize the past, find counts, trends, etc. This tool can be used to reduce development time, assist in
dashboard creation, and ultimately reduce the burden on teams answering data-driven questions in Slack. 

As part of this initial release, only Postgres is supported.

## How it works

```
Janet, which customer has the most invoices?

Result:
{
  "FirstName": "Alexandre",
  "LastName": "Rocha",
  "count": "7"
}

```

TODO

## Best Practices

### Least Privilege

Please only give Janet the least amount of privilege required to answer your questions. Our recommendation is to:

1. Create a seperate database user
2. Supply a read-only connection
3. Restrict who has access to call Janet's APIs

### Smallest Preload

It's recommended that you preload subsets of your database schema to answer specific and/or frequent questions. This reduces the size of the prompt sent to OpenAI, which will save you money
and improve the accuracy of the results. In addition, it'll prevent you from accidentally exposing sensitive table ddl, if that's a consideration for you and your team (note: Janet will never
send actual table data to OpenAI).

## HTTP API 

### POST /api/preload 

Load and cache a subset of your database schema. 

Janet will fetch tables matching the filters. The ddl will be saved to disk and can be used when calling `/api/question`. See `/api/question` for more details.

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
curl -X POST -H "Content-Type: application/json" -d "{ \"name\": \"public\" }" http://localhost:3000/api/preload
```

### POST /api/question

Ask a basic analytics question, and get back the results. The query Janet used to generate the results will be attached as well, for review and verification.

If a `preloadName` is not passed, then it'll call `/api/preload` beforehand. To lower usage costs and improve accuracy, it's recommended you preload beforehand and only include the smallest subset of tables required to answer the question.

If OpenAI returns multiple responses (default 3, configurable using the 'openaiParams' field), then the first query that succeeds will be taken.

Request body

```typescript
{
  question: string,
  preloadName?: string, // makes a default call to /api/preload, but doesn't persist the result.
  runQuery?: boolean, // defaults to true 
  openaiParams?: Record<string, any> // defaults to { "model": "text-davinci-003", "temperature": 0.2, "n": 3, "max_tokens": 32 } 
}
```

Example

```sh
curl -X POST -H "Content-Type: application/json" -d "{ \"preloadName\": \"public-schemas\", \"question\": \"How many employees were hired in 2003?\" }" http://localhost:3000/api/question
```
