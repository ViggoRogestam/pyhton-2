import pytest
import urllib.request as request
import ssl
import flask
from application.app import app


context = ssl._create_unverified_context()

def test_Is_online_index():
    """
    Denna funktion testar om servern är online genom att göra ett anrop mot endpoint '/'.
    """
    assert request.urlopen("http://127.0.0.1:5000", context=context, timeout=10)

def test_Is_online_form():
    """
    Denna funktion testar om servern är online genom att göra ett anrop mot endpoint '/form'.
    """
    assert request.urlopen("http://127.0.0.1:5000/form", context=context, timeout=10)

def test_api_route_is_online():
    """
    Denna testcase testar om endpoint '/api' returnerar statuskoden 200
    """
    assert request.urlopen("http://127.0.0.1:5000/form", context=context, timeout=10)






    # with app.test_request_context('/api', method='POST', data={'year': '2022', 'month': '12', 'day': '31', 'price_class': 'SE3'}):
    #     response = urllib.request(f"https://www.elprisetjustnu.se/api/v1/prices/{2022}/{12}-{31}_{SE3}.json")
        # assert response.status_code == 200
        # assert b'Resultat' in response.headline
      

# def test_catch_404():
#     with request.urlopen("http://127.0.0.1:5000/log", context=context, timeout=10) as response:
#         html = str(response.read())
#         assert "<h1>Sidan du söker finns inte</h1>" in html

#TODO: testcase för post på api
#TODO: testcase att se att data för visst datumn stämmer
#TODO: göra testcase för funktionerna i app.py
