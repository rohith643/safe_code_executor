from flask import Flask, request, jsonify
from runner import run_code
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

MAX_CODE_LENGTH = 5000  # basic limit

@app.post("/run")
def run():
    data = request.get_json(silent=True) or {}
    code = data.get("code", "")

    if not isinstance(code, str) or not code.strip():
        return jsonify(error="No code provided"), 400

    if len(code) > MAX_CODE_LENGTH:
        return jsonify(error="Code exceeds 5000 characters"), 413  # Payload Too Large

    result = run_code(code)
    return jsonify(result), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
