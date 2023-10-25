from flask import Flask
from flask import Flask, render_template, request
import urllib3 as urlrequest
import pandas as pd
import json
import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)
