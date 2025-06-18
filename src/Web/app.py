import os
import requests
from flask import *
from identity.flask import Auth

import app_config

app = Flask(__name__)
app.config.from_object(app_config)
auth = Auth(
    app,
    authority=app_config.AUTHORITY,
    client_id=app_config.CLIENT_ID,
    client_credential=app_config.CLIENT_SECRET,
    redirect_uri=app_config.REDIRECT_URI
)

@app.route('/')
def index():
    print('Request for index page received', app_config.CLIENT_ID)
    return render_template('index.html', title='Home')

@app.route('/welcome')
@auth.login_required
def welcome():
    return render_template('welcome.html', title='Welcome')

if __name__ == '__main__':
    app.run()