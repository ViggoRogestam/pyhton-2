from flask import Flask, jsonify, request
import pandas as pd


app = Flask(__name__)


@app.route("/")
def show_lust():
    dict = {
        "landskap": ["Östergötland", "Östergötland", "Västergötland", "Södermanland", "Södermandland", "Norrbotten", "Gästrikland", "Ångermanland", "Ångermanland", "Ångermandland"],
        "landsdel": ["Götaland", "Götaland", "Götaland", "Svealand", "Svealand", "Norrland", "Norrland", "Norrland", "Norrland", "Norrland"],
        "stad": ["Linköping", "Motala", "Mjölby", "Mariefred", "Nyköping", "Piteå", "Sandviken", "Sollefteå", "Kramfors", "Önrsköldsvik"],
    }


df = pd.from_dict(dict)
