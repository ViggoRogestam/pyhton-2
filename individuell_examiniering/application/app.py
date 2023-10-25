from flask import Flask
from flask import Flask, render_template, request
import urllib as urlrequest
import pandas as pd
import json
import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/form')
def form():
    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)
