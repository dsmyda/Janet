# <img style="background:white; border-radius: 12px;" src="https://user-images.githubusercontent.com/12688453/229330427-fc12979a-443d-43c7-8e3f-2938cd5e3b78.png"  width="24" height="24"> openquery

openquery is an open source automated descriptive analytics system. It works by translating natural language queries into SQL, using your database schema to generate viable solutions. You can opt-in to automatically run those SQL queries for a nice end-to-end experience.

openquery is designed with information security in mind, and plans to support automated PII detection for your database schema and natural language queries.

Still under active development. Currently supports OpenAI and Postgres.

demo: TBD

## Features

- Supports OpenAI language models
- Built-in AST for query validation & correction
- Supports 19+ dialects, including Postgres, Presto, BigQuery and Snowflake
- Built-in PII detection to prevent accidental data leaks

## How it works

TODO - Add a diagram

## Best Practices

### Least Privilege

openquery should only be given the least amount of privilege required to answer your questions. Our recommendation

1. Create a seperate database user, with sane RBAC
2. Supply a read-only connection
3. Restrict who has access to openquery's APIs

### Minimal Synthesis

It's recommended that you synthesize subsets of your database schema to answer specific and/or frequent questions. This reduces the context length, saving you money and ensuring broad model support. 

### Don't use PII

In most cases, you can rephrase your query to eliminate PII. Take the following example

_BAD_
```
How many total invoices do we have for john.doe@gmail.com?
```

_BETTER_
```
How many total invoices do we have for emails starting with 'joe' and ending with '@gmail.com'?
```

_IDEAL_
```
How many total invoices do we have for user id ea916801-2987-4f29-aab5-f2b1061dc8f4?
```

## HTTP API 

### POST /api/synthesize 

Digest and cache a subset of your database schema. 

openquery will fetch tables matching the filter criteria. The results will be saved to disk and can be referenced when calling `/api/question`. See `/api/question` for more details.

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
curl -X POST -H "Content-Type: application/json" -d "{ \"name\": \"public\" }" http://localhost:3000/api/synthesize
```

### POST /api/question

Ask a basic analytics question. The query used to produce the results will be attached, for review and verification.

If `synthName` is not passed, then it'll call `/api/synthesize`. To lower usage costs and improve accuracy, it's recommended you synthesize the smallest subset of tables required to answer the question.

If OpenAI returns multiple responses (default 3, configurable using the `openaiParams` field), then the first query that succeeds will be taken.

Request body

```typescript
{
  question: string,
  synthName?: string, // makes a default call to /api/synthesize, but doesn't persist the result.
  runQuery?: boolean, // defaults to true 
  openaiParams?: Record<string, any> // defaults to { "model": "text-davinci-003", "temperature": 1, "n": 3, "max_tokens": 32 } 
}
```

Example

```sh
curl -X POST -H "Content-Type: application/json" -d "{ \"synthName\": \"public-schemas\", \"question\": \"How many employees were hired in 2003?\" }" http://localhost:3000/api/question
```

## Slack

TODO

## Discord
