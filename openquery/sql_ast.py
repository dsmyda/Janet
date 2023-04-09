from sqlglot import parse_one, exp, Dialect, TokenType

_mutation_tokens = (
    TokenType.COMMAND,
    TokenType.INSERT,
    TokenType.UPDATE,
    TokenType.ALTER,
    TokenType.REPLACE,
    TokenType.OVERWRITE,
    TokenType.DROP,
    TokenType.DELETE,
    TokenType.CREATE
)

def is_query(sql: str):
    tokens = Dialect.get_or_raise(None)().tokenize(sql)
    return all(token.token_type not in mutation_tokens for token in tokens)

def standardize(sql: str):
    ast = parse_one(sql)

    def transformer(node):
        if isinstance(node, exp.Identifier):
            return node if node.quoted else parse_one("\"{}\"".format(node.sql()))
        return node

    return ast.transform(transformer).sql(pretty=True)

def has_pii(sql: str):
    ast = parse_one(sql)
    for expression, *_ in ast.walk():
        if isinstance(expression, exp.Identifier):
            pass
        
    return False