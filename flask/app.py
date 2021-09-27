from flask import Flask
from waitress import serve
from flask import render_template
from flask import request,url_for,send_from_directory,redirect,flash,session
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
bootstrap = Bootstrap(app)
CSRFProtect(app)

@app.route('/')
def root():
    return ("Ola mundo!")

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=80, url_prefix='/app')