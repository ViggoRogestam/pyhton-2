from flask import Flask
from flask import Flask, render_template, request
import urllib.request as urlrequest
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


@app.route('/api', methods=['POST'])
def api():
    """
    Denna funktion körs när man går till endpoint '/api'.
    Den tar endast emot trafik med HTTP method post.
    Den hämtar datan från formuläret och skickar den till api:et.
    """
    # Hämta data från formuläret
    year = request.form['year']
    month = request.form['month']
    day = request.form['day']
    price_class = request.form['price_class']

    # Gör ett anrop mot api:et och spara ner resultatet
    data = urlrequest.urlopen(
        f"https://www.elprisetjustnu.se/api/v1/prices/{year}/{month}-{day}_{price_class}.json").read()
    # Gör om resultatet från json till en lista av dictionaries
    formated_data = json.loads(data)
    # Gör om formated_data till en pandas dataframe och sedan till html med hjälp av to_html()  
    df = pd.DataFrame(formated_data)
    df_html = df.to_html(
        classes="table table-striped table-hover table-bordered table-sm", index=False)

    return render_template('base.html', data=df_html, headline="Resultat ")

if __name__ == '__main__':
    app.run(debug=True)
