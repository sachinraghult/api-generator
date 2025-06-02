from flask import Flask, Response, request, jsonify
import time

app = Flask(__name__)

@app.route("/api/sample", methods=["GET", "POST"])
def mcp_handler():
    if request.method == "GET":
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

# ➕ Add SSE route for DevX agent to hook into
@app.route('/events')
def stream():
    def event_stream():
        yield 'data: {"status": "connected"}\n\n'
        while True:
            time.sleep(15)  # keep-alive ping
            yield 'data: {"ping": true}\n\n'

    return Response(event_stream(), mimetype="text/event-stream")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
