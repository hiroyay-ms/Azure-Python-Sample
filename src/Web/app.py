import requests
import uuid
from flask import *
from flask_session import Session
import msal

import app_config

app = Flask(__name__)
app.config.from_object(app_config)
Session(app)

@app.route('/')
def index():
    print('Request for index page received', app_config.CLIENT_ID)
    return render_template('index.html', title='Home')

@app.route('/welcome')
def welcome():
    if not session.get("user"):
        return redirect(url_for("login"))
    return render_template('welcom.html', title='Welcome', user=session["user"])

def _build_msal_app(cache=None):
    return msal.ConfidentialClientApplication(
        app_config.CLIENT_ID,
        authority=app_config.AUTHORITY,
        client_credential=app_config.CLIENT_SECRET,
        token_cache=cache
    )

def _load_cache():
    cache = msal.SerializableTokenCache()
    if session.get("token_cache"):
        cache.deserialize(session["token_cache"])
    return cache

def _save_cache(cache):
    if cache.has_state_changed:
        session["token_cache"] = cache.serialize()

@app.route('/getAToken')
def authorized():
    if request.args['state'] != session.get("state"):
        return redirect(url_for("login"))
    cache = _load_cache()
    result = _build_msal_app(cache).acquire_token_by_authorization_code(
        request.args['code'],
        scopes=app_config.SCOPE,
        redirect_uri=url_for("authorized", _external=True)
    )
    session["user"] = result.get("id_token_claims")
    _save_cache(cache)
    return redirect(url_for("index"))

@app.route('/login')
def login():
    session["state"] = str(uuid.uuid4())
    auth_url = _build_msal_app().get_authorization_request_url(
        app_config.SCOPE,
        state=session["state"],
        redirect_uri=url_for("authorized", _external=True)
    )
    return redirect(auth_url)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(
        app_config.AUTHORITY + "/oauth2/v2.0/logout" +
        "?post_logout_redirect_uri=" + url_for("index", _external=True)
    )

if __name__ == '__main__':
    app.run()