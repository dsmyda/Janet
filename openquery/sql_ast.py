from sqlglot import parse_one, exp, Dialect, TokenType

mutation_tokens = (
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

class AST:
    
    def __init__(self, sql: str):
        self._ast = parse_one(sql)
        self._raw_sql = sql
        self._dialect = Dialect.get_or_raise(None)()

    def is_query(self):
        tokens = self._dialect.tokenize(self._raw_sql)
        return all(token.token_type not in mutation_tokens for token in tokens)

    def standardize(self):

        def transformer(node):
            if isinstance(node, exp.Identifier):
                return node if node.quoted else parse_one("\"{}\"".format(node.sql()))
            return node

        self._ast = self._ast.transform(transformer)

    def has_pii(self):
        for expression, *_ in self._ast.walk():
            if isinstance(expression, exp.Identifier):
                pass

    def to_sql(self):
        return self._ast.sql()
