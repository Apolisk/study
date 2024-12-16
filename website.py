from flask import Flask, jsonify, request
from main import decrease_url, expand_url, login, users
from urllib.parse import unquote
app = Flask(__name__)

@app.route("/decrease_url/<int:user_id>", methods=['GET', 'POST'])
def decr(user_id):
    if request.method == "GET":
        long_url = request.args.get("long_url")
        long_url = unquote(long_url)
        if login(user_id):
            result = decrease_url(user_id,long_url)
            if result:
                return jsonify({"response": 201, "short_url": result}), 201
            else:
                return jsonify({"response": 400, "message": "Failed to short URL"}), 400
        else:
            return jsonify({"response": 401, "message": "Unauthorized"}), 401

    if request.method == "POST":
        data = request.get_json()
        long_url = data.get("long_url")
        if not long_url:
            return jsonify({"response": 400, "message": "Missing long_url in request"}), 400
        if login(user_id):
            result = decrease_url(user_id, long_url)
            if result:
                return jsonify({"response": 201, "short_url": result}), 201
            else:
                return jsonify({"response": 400, "message": "Failed to shorten URL"}), 400
        else:
            return jsonify({"response": 401, "message": "Unauthorized"}), 401

@app.route("/expand_url/<int:user_id>")
def expn(user_id):
    short_url = request.args.get("short_url")
    if login(user_id):
        result = expand_url(user_id,short_url)
        if result:
            return jsonify({"response": 302, "redirect": result}), 302
        else:
            return jsonify({"response": 400, "message": "Missing long_url"}), 400
    else:
        return jsonify({"response": 404, "message": "URL not found"}), 404

@app.route("/users")
def get_all_users():
     return users