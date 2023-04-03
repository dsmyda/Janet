def parse():
  # SQLGlot parse_one
  pass

def fix_quotes():

  def transformer(node):
    if isinstance(node, exp.Identifier):
        return parse_one("\"{}\"".format(node.sql()))
    return node
  
  # Transform SQLGlot AST to properly quote all identifiers
  pass

def is_query():
  # Traverse SQLGlot AST to determine if query is a SELECT
  pass

def has_pii(expression):

  found_pii = False

  if isinstance(expression, exp.Identifier):
    if is_pii(expression.sql()):
      found_pii = True

  return found_pii or any(has_pii(child) for child in expression.children)