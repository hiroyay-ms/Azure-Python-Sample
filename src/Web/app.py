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



if __name__ == '__main__':
    app.run()