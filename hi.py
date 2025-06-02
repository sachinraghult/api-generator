# FILE: app.py
from flask import Flask, jsonify, request
import uuid
import time

app = Flask(__name__)

@app.route('/api/sample', methods=['GET'])
def get_sample():
    """
    A basic GET API endpoint that returns a sample JSON response with MCP context.
    """

    # --- Minimal MCP Context ---
    mcp_context = {
        "mcp_version": "1.0",
        "request_id": str(uuid.uuid4()),
        "endpoint": request.path,
        "method": request.method,
        "timestamp": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    }

    # You can optionally include this in the response for traceability
    response = {
        "message": "Hello, this is a sample GET API!",
        "status": "success",
        "mcp_context": mcp_context
    }

    return jsonify(response), 200


if __name__ == '__main__':
    app.run(debug=True)






from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/api/sample", methods=["POST"])
def mcp_handler():
    data = request.get_json(force=True)

    # Validate JSON-RPC 2.0 basic structure
    if not data or "jsonrpc" not in data or data["jsonrpc"] != "2.0":
        return jsonify({
            "jsonrpc": "2.0",
            "error": {
                "code": -32600,
                "message": "Invalid Request"
            },
            "id": data.get("id") if data else None
        }), 400

    method = data.get("method")
    params = data.get("params", {})
    request_id = data.get("id")

    # Sample implementation
    if method == "get_hello":
        result = {"message": "Hello from MCP local server!"}
    else:
        return jsonify({
            "jsonrpc": "2.0",
            "error": {
                "code": -32601,
                "message": f"Method '{method}' not found"
            },
            "id": request_id
        }), 404

    return jsonify({
        "jsonrpc": "2.0",
        "result": result,
        "id": request_id
    }), 200

if __name__ == "__main__":
    app.run(debug=True)







from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/api/sample", methods=["GET", "POST"])
def mcp_handler():
    if request.method == "GET":
        # Used by DevX agent to validate the server is up
        return jsonify({"status": "ok"}), 200

    data = request.get_json(force=True)
    if not data or data.get("jsonrpc") != "2.0":
        return jsonify({
            "jsonrpc": "2.0",
            "error": {
                "code": -32600,
                "message": "Invalid Request"
            },
            "id": data.get("id") if data else None
        }), 400

    method = data.get("method")
    params = data.get("params", {})
    request_id = data.get("id")

    if method == "get_hello":
        result = {"message": "Hello from MCP local server!"}
    else:
        return jsonify({
            "jsonrpc": "2.0",
            "error": {
                "code": -32601,
                "message": f"Method '{method}' not found"
            },
            "id": request_id
        }), 404

    return jsonify({
        "jsonrpc": "2.0",
        "result": result,
        "id": request_id
    }), 200

if __name__ == "__main__":
    app.run(debug=True)
