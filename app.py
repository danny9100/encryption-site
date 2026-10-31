# app.py
from flask import Flask, request, jsonify, render_template
from cipher import encrypt, decrypt

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/encrypt", methods=["POST"])
def api_encrypt():
    data = request.get_json(silent=True) or {}
    text = data.get("text", "")
    key = data.get("key", "")
    if not text or not key:
        return jsonify({"error": "Both 'text' and 'key' are required"}), 400
    try:
        return jsonify({"result": encrypt(text, key), "status": "success"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/decrypt", methods=["POST"])
def api_decrypt():
    data = request.get_json(silent=True) or {}
    text = data.get("text", "")
    key = data.get("key", "")
    if not text or not key:
        return jsonify({"error": "Both 'text' and 'key' are required"}), 400
    try:
        return jsonify({"result": decrypt(text, key), "status": "success"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True)