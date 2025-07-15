# code using flask backend and RESTful api

from flask import Flask, request, jsonify
import graphene

app = Flask(__name__)


@app.route('/')
def home():
    return "Welcome to Calculator API"

@app.route('/add', methods=['GET'])
def add():
    a = request.args.get('a', type=float)
    b = request.args.get('b', type=float)
    result = a + b
    return jsonify({'result': result})

@app.route('/subtract', methods=['GET'])
def subtract():
    a = request.args.get('a', type=float)
    b = request.args.get('b', type=float)
    result = a - b
    return jsonify({'result': result})

@app.route('/multiply', methods=['GET'])
def multiply():
    a = request.args.get('a', type=float)
    b = request.args.get('b', type=float)
    result = a * b
    return jsonify({'result': result})

@app.route('/divide', methods=['GET'])
def divide():
    a = request.args.get('a', type=float)
    b = request.args.get('b', type=float)
    if b == 0:
        return jsonify({'error': 'Division by zero not allowed'}), 400
    result = a / b
    return jsonify({'result': result})




# ----------------------- JSON-RPC Endpoint -----------------------
@app.route('/rpc', methods=['POST'])
def handle_rpc():
    data = request.get_json()
    
    # Validate request
    if not data or "method" not in data:
        return jsonify({"jsonrpc": "2.0", "error": "Invalid Request", "id": data.get("id")}), 400

    method = data["method"]
    params = data.get("params", [])
    req_id = data.get("id")

    try:
        if method == "add":
            result = sum(params)
        elif method == "subtract":
            result = params[0] - params[1]
        elif method == "multiply":
            result = params[0] * params[1]
        elif method == "divide":
            if params[1] == 0:
                raise ValueError("Division by zero")
            result = params[0] / params[1]
        else:
            return jsonify({"jsonrpc": "2.0", "error": "Method not found", "id": req_id}), 400

        return jsonify({"jsonrpc": "2.0", "result": result, "id": req_id})

    except Exception as e:
        return jsonify({"jsonrpc": "2.0", "error": str(e), "id": req_id}), 500


# ----------------------- GraphQL Schema -----------------------

class Calculator(graphene.ObjectType):
    add = graphene.Float(a=graphene.Float(), b=graphene.Float())
    subtract = graphene.Float(a=graphene.Float(), b=graphene.Float())
    multiply = graphene.Float(a=graphene.Float(), b=graphene.Float())
    divide = graphene.Float(a=graphene.Float(), b=graphene.Float())

    def resolve_add(root, info, a, b):
        return a + b

    def resolve_subtract(root, info, a, b):
        return a - b

    def resolve_multiply(root, info, a, b):
        return a * b

    def resolve_divide(root, info, a, b):
        if b == 0:
            raise Exception("Division by zero")
        return a / b

schema = graphene.Schema(query=Calculator)


@app.route("/graphql", methods=["POST"])
def graphql_endpoint():
    data = request.get_json()
    result = schema.execute(
        data.get("query"),
        variables=data.get("variables")
    )
    return jsonify(result.data if result.data else {"errors": [str(e) for e in result.errors]})


# ----------------------- Run App -----------------------

if __name__ == '__main__':
    app.run( port =8080) 
