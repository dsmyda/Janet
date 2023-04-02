# <img style="background:white; border-radius: 12px;" src="https://user-images.githubusercontent.com/12688453/229330427-fc12979a-443d-43c7-8e3f-2938cd5e3b78.png"  width="24" height="24"> openquery

openquery is an open source automated descriptive analytics system. It works by translating natural language queries into SQL, using your database schema to generate viable solutions. You can opt-in to automatically run those SQL queries for a nice end-to-end experience.

openquery is designed with information security in mind, and supports automated PII detection for your database schema and natural language queries.

demo: TBD

## Installation

TODO - add installation for openquery cli binary

## Features

- OpenAI language models
- Built-in AST for query correction in 20+ dialects, including Postgres, Presto, BigQuery and Snowflake
- Schema introspection and query execution in 5 dialects, with community support for 10+ others
- Support for quering CSV and TSV files (planned)
- Built-in PII detection to prevent accidental data leaks (planned)
- Integration with Discord and Slack (planned)

## How it works

### Concepts

- Profiles (TBD - allows for easy switching between remote dbs)
- Synth

## Best Practices

### Least Privilege

openquery should only be given the least amount of privilege required to answer your questions. Our recommendation

1. Create a seperate database user, with defensive RBAC
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

_GOOD_
```
How many total invoices do we have for user with id 'ea916801-2987-4f29-aab5-f2b1061dc8f4'?
```

openquery has built-in pii detection to prevent these kind of mistakes.
