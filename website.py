from urllib.parse import unquote
from flask import Flask
from main import decrease_url, expand_url, login, users

app = Flask(__name__)

@app.route("/decrease_url/<int:user_id>/<string:long_url>")
def decr(user_id, long_url):
    long_url = unquote(long_url)
    if login(user_id):
        result = decrease_url(user_id,long_url)
        if result:
            return f"Here your short url: {result}"
        else:
            return f"Can't save url"
    else:
        return f"User with ID: {user_id} does not exist"

@app.route("/expnad_url/<int:user_id>/<string:short_url>")
def expn(user_id, short_url):
    if login(user_id):
        result = expand_url(user_id,short_url)
        if result:
            return f"Here your long url: {result}"
        else:
            return f"No long url saved"
    else:
        return f"User with ID: {user_id} does not exist"

@app.route("/users")
def get_all_users():
     return users