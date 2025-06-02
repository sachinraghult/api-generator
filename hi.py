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
