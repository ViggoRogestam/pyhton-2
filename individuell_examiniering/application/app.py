from flask import Flask
from flask import Flask, render_template, request
import urllib.request as urlrequest
from urllib.error import HTTPError, URLError
from application import func
import pandas as pd

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


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

    # kolla om månad eller dag är ensiffriga, isf lägg till en nolla framför
    if len(str(month)) < 2:
        month = '0' + month
    if len(str(day)) < 2:
        day = '0' + day
    # Gör ett anrop mot api:et
    # se om svaret ger statuskod 200 eller om det blir något fel
    try:
        response = urlrequest.urlopen(
            f"https://www.elprisetjustnu.se/api/v1/prices/{year}/{month}-{day}_{price_class}.json")
    # om det blir en error så skicka tillbaka ett felmeddelande
    # om error är 404 skicka tillbaka att datumet inte finns i databasen annars skicka tillbaka error med statuskod
    except HTTPError as e:
        if e.code == 404:
            error = 'Det inmatade datumet finns inte i databasen'
            return render_template('error.html', error=error)
        else:
            error = ('HTTP error. Status code: ', e.code)
    except URLError as e:
        error = ('URL error. Reason: ', e.reason)
        return render_template('error.html', error=error)
    # om ingen error så fortsätt
    else:
        # gör om svaret till en pandas dataframe
        df = func.respone_to_df(response)

        # Modifiera dataframen
        ## byter namn på kolumnerna
        rename_dict = {'SEK_per_kWh': 'Kronor/kWh',
                       'EUR_per_kWh': 'Euro/kWh'}
        func.rename_dr(df, rename_dict)
        ## bryter ut datum och tid från time_start
        ## skapar en variabel med valt datum
        date = func.extract_date_from_dataframe(df)
        ## skapar en ny column för tid och tar bort onödiga columner
        df = func.create_time_column(df)
        # Gör om dataframet till html
        df_html = func.df_to_html(df)
        # Skicka med datan till template
        return render_template('api.html', data=df_html, headline="Resultat", date=date,)

# Fånga 404 error och skicka tillbaka en egen sida
@app.errorhandler(404)
def not_found_error(e):
    error = 'Sidan du söker finns inte'
    return render_template('404.html', data=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
