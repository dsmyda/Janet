# <img style="background:white; border-radius: 12px;" src="https://user-images.githubusercontent.com/12688453/229330427-fc12979a-443d-43c7-8e3f-2938cd5e3b78.png"  width="24" height="24"> openquery

openquery is an open source automated descriptive analytics tool. It works by translating natural language queries into SQL, using your database schema to generate viable solutions. You can opt-in to automatically run those SQL queries for a nice end-to-end experience.

openquery is designed with information security in mind, and supports automated PII detection for your database schema and natural language queries.

demo: TBD

## Installation

TODO - add installation for openquery cli binary

brew install openssl

export LDFLAGS="-L/opt/homebrew/opt/openssl@3/lib"
export CPPFLAGS="-I/opt/homebrew/opt/openssl@3/include"

## Features

- OpenAI language models
- Query parser supporting 20+ dialects, including Postgres, Presto, BigQuery and Snowflake
- Schema introspection and query execution in 5 dialects, with community support for 10+ others
- PII detection to prevent accidental data leaks
- Support for quering CSV and TSV files (planned)
- Integration with Discord and Slack (planned)

## How it works

### Concepts

- Profile
- Synth
  - Structures like tables, views, indexes and foreign keys are synth'd
  - Structures like CHECK constraints, table comments, and triggers are not synth'd.
- Language Model

## Best Practices

### Least Privilege

openquery should only be given the least amount of privilege required to answer your questions. Our recommendation

1. Create a seperate database user, with defensive RBAC
2. Use a read-only connection

while openquery ships with many [safety checks](/#), you should not rely solely on openquery to catch all edge cases.

### Smallest Synth

It's recommended that you synth the smallest subset of tables needed to produce complete queries. This reduces the context length, saving you money and ensuring broad model support. 

### Don't use PII

In most cases, you can rephrase your query to eliminate PII. Take the following example

_BAD_
```
How many total invoices do we have for john.doe@gmail.com?
```

_GOOD_
```
How many total invoices do we have for user with id ea916801-2987-4f29-aab5-f2b1061dc8f4?
```

openquery has built-in pii detection to prevent these kind of mistakes.
