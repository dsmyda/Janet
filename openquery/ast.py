import sqlglot

class AST:
    
    def __init__(self, sql: str):
        self._ast = sqlglot.parse_one(sql)

    def is_query(self):
        pass

    def fix_common_mistakes(self):

        def transformer(node):
            if isinstance(node, exp.Identifier):
                return parse_one("\"{}\"".format(node.sql()))
            return node

        pass
    
    def detect_pii(self):
        def visit(expression): 
            if isinstance(expression, exp.Identifier):
                pass

            return any(visit(child) for child in expression.children)

        visit(self._ast)

    def to_sql(self):
        pass
