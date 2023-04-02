def parse():
  # SQLGlot parse_one
  pass

def quote():

  def transformer(node):
    if isinstance(node, exp.Identifier):
        return parse_one("\"{}\"".format(node.sql()))
    return node
  
  # Transform SQLGlot AST to properly quote all identifiers
  pass

def is_query():
  # Traverse SQLGlot AST to determine if query is a SELECT
  pass

def has_pii():
  # Traverse SQLGlot AST to determine if query has PII
  pass

def optimize():
  # SQLGlot optimize
  pass
