from sqlglot import exp, parse_one
from flask import Flask
from flask import request

app = Flask(__name__)

def transformer(node):
    if isinstance(node, exp.Identifier):
        return parse_one("\"{}\"".format(node.sql()))
    return node

@app.route("/transform", methods=["POST"])
def transform():
    body = request.get_json()
    try:
        expression_tree = parse_one(body["query"])
        transformed_tree = expression_tree.transform(transformer)
        return {
            "code": 200,
            "original": body["query"],
            "transformed": transformed_tree.sql()
        }
        return transformed_tree.sql()
    except Exception as e:
        return {
            "code": 500,
            "error": str(e),
            "original": body["query"],
        }