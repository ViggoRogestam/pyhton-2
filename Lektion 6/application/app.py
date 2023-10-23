# Den här filen innehåller saker som har med Flask-servern att göra, det vill säga endpoints, routing, HTTP-metoder etc.
# Flask innehåller all funktionalitet för att skapa en server och hantera trafik till och från den servern, men inte funktionalitet
# för att skicka requests till andra servrar. Till detta använder vi i func.py istället urllib vilket är ett av pythons standardbibliotek.

# Termer: Bibliotek, standardbilbliotek, ramverk och moduler refererar ofta till samma sak, dvs. förbyggd kod som du kan importera.
# Ett standardbibliotek är ett som levereras som en del av Pyhton, och de är ofta 'native python' el. med andra ord skrivna helt i python
# Andra bibliotek kan vara skrivna med en annan miljö i bakgrunden, t.ex med C. Dessa bibliotek kan vara plattformsberoende (win, linux, mac osv)
# medan bibliotek i native python är platformsoberoende och kan användas överallt där bythonkod kan köras.

from markupsafe import escape
from application import func
from flask import Flask, render_template, request
from urllib import request as urlrequest
import json
import datetime
# Skapa ett Flask server-objekt. Det är denna som ni sedan startar med 'flask run' från terminalen.
app = Flask(__name__)


@app.route("/")
def index():
    '''Denna funktion körs när man går till servern utan endpoint. 
       På en statisk webbsida skulle detta t.ex motsvara filen index.html'''

    ##### Plats för er kod #####
   # 1. Hämta besökarens IP adress, samt countrycode genom ett anrop till CloudFlare's API https://
    api_info = urlrequest.urlopen("https://1.1.1.1/cdn-cgi/trace").read()
   # 2. Använd python för att bryta ut informationen ur resultatet och spara ner dessa värden i variabler.
    parts = str(api_info).split()
    ip = None
    loc = None
    for part in parts:
        if part.startswith("ip="):
            ip = part[3:]
        elif part.startswith("loc="):
            loc = part[4:]
   # 3. Get current year
    current_year = datetime.datetime.now().year
   # 4. Posta mot api med ip och loc och gör om från json till html table
    data_url = f"https://date.nager.at/api/v3/PublicHolidays/{current_year}/{loc}"
    data = func.json_url_to_html_table(data_url)
    # Hämta index.html och uppdatera den med hjälp av Jinja, skicka den sedan till klienten (browsern)
    return render_template('index.html', data=data)


@app.route("/form")
def form():
    '''Denna funktion körs när man går till servern med  endpoint '/form'. 
       På en statisk webbsida skulle detta t.ex kunna motsvara filen mappen /form med filen index.htm'''

    ##### Plats för er kod #####
    # 1. Hämta alla tillgängliga länder från API:et https://date.nager.at/swagger/index.html
    api_countrys = urlrequest.urlopen(
        "https://date.nager.at/api/v3/AvailableCountries")
    # 2. Gör om hämtat resultat från json till en lista av dictionaries
    dict_countrys = json.loads(api_countrys.read())

    return render_template('form.html', dict_countrys=dict_countrys)


@app.route("/api", methods=["POST"])
def api_post():
    '''Denna funktion körs när man går till servern med  endpoint '/api'. 
       Den tar endast emot trafik med HTTP method post.
       Försöker man med en annan metod, t.ex get, så körs den alltså inte.'''

    ##### Under lektion_4 skapade vi kod här för att göra göra om json från ett externt API, till en HTML-tabell med Pandas #####
    ##### Här har anropet till API:et samt omvandlingen flyttats ut till en egen funktion i filen func.py                   #####

    # Flask-kod sparar vi i app.py. Objectet request från flask innehåller den HTTP request som i det här fallet skickades till /api
    # Läs innehållet från request som motsvarar <input> med name= 'year' samt 'countrycode' i HTML-formuläret <form> (form.html)
    """
    year = request.form["year"]
    country_code = request.form["countryCode"]
    """

    # Skapa URL för det API vi skall använda, med en formaterad sträng och injecera variablerna year, samt country_code
    data_url = f"https://date.nager.at/api/v3/PublicHolidays/{request.form['year']}/{request.form['countryCode']}"

    # Använd nu den kod vi brutit ut och lagt till i func.py för att utföra arbetet
    data = func.json_url_to_html_table(data_url)

    # Skicka tillbaka resultatet till browsern med Jinja, dvs uppdatera mallen index.html med innehållet i variabeln data
    return render_template('index.html', data=data)


@app.route("/api/xml")
def xml():
    '''Denna funktion körs när man går till servern med  endpoint '/api/xml'. 
       Den tar endast emot trafik med alla HTTP methods.
       Den gör samma sak som funktionen ovan (api_post()) men med XML istället för JSON.'''

    # I det här exemplet har vi inga argument att lägga in i API:ets URL, så vi använder en vanlig sträng.
    # XPath är ett sätt att navigera i XML. Raden nedan väljer ut alla taggar med namn <item>
    data_url = "https://polisen.se/aktuellt/rss/stockholms-lan/handelser-rss---stockholms-lan/"
    data = func.xml_url_to_html_table(data_url, xpath="//item")

    # Skicka tillbaka resultatet till browsern med Jinja, dvs uppdatera mallen index.html med innehållet i variabeln data
    return render_template('index.html', data=data)
