import json
import os
import requests
import urllib
from flask import Flask, request, redirect


HEROKU_ID = os.environ.get('HEROKU_ID')
HEROKU_SECRET = os.environ.get('HEROKU_SECRET')

app = Flask(__name__)

@app.route('/')
def index():
    params = dict(
        client_id=HEROKU_ID,
        response_type='code',
        state='1234', # TODO: Gen random number
        scope='global'
    )
    if 'code' not in request.args:
        return redirect('https://id.heroku.com/oauth/authorize?' + 
            urllib.urlencode(params))
    params = dict(
        grant_type='authorization_code',
        code=request.args['code'],
        client_secret=HEROKU_SECRET
    )
    response = requests.post('https://id.heroku.com/oauth/token', data=params)
    data = json.loads(response.text)
    if 'access_token' not in data:
        return 'Error: ' + data['message']
    return """<html>
        <head></head>
        <body>
            <script type="text/javascript">
                localStorage.setItem('access_token', '{0}');
                window.close();
            </script>
        </body>
    </html>
    """.format(data['access_token'])

@app.route('/embed')
def embed():
    return """<html>
        <head></head>
        <body>
            <script type="text/javascript">
                window.addEventListener('storage', function(event) {
                    window.top.postMessage(event.newValue, '*');
                });
            </script>
        </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=True) 