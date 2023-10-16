from flask import Flask
anteckning_1 = "gå till läkaren"
app = Flask(__name__)

@app.route('/')
def route():
    """Returnera en sida med anteckningar."""
    page =f"""
<!DOCTYPE html>
<html>
    <body style="background-color:grey;">

    <h1 style="color:white;"> Viggos anteckningslista</h1>
    <p style="color:green;"> - städa.</p>
    <p style="color:white;"> - laga mat.</p>
    <p style="color:yellow;"> - träna.</p>
    <p> - {anteckning_1}</p>
    
    </body>
</html> 
"""
    return page