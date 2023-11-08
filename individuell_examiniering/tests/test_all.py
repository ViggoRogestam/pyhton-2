import pytest
import urllib.request
import ssl
from application import app

context = ssl._create_unverified_context()

def test_Is_online_index():
    """
    Denna funktion testar om servern är online genom att göra ett anrop mot endpoint '/'.
    """
    assert urllib.request.urlopen("http://127.0.0.1:5000", context=context, timeout=10)

def test_Is_online_form():
    """
    Denna funktion testar om servern är online genom att göra ett anrop mot endpoint '/form'.
    """
    assert urllib.request.urlopen("http://127.0.0.1:5000/form", context=context, timeout=10)

def test_index(client):
    """
    Denna testcase testar om endpoint '/' returnerar statuskoden 200
    och om den returnerar en title med texten 'index'.
    """
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200
        assert b"<title>index</tilte>" in response.data
    
def test_form_route():
    """
    Denna testcase testar om endpoint '/form' returnerar statuskoden 200
    och om den returnerar en h1 med texten 'Form'.
    """
    with app.test_client() as client:
        response = client.get('/form')
        assert response.status_code == 200
        assert b"<h1>Form</h1>" in response.data

#TODO: def test_api():
    # with app.test_request_context('/api', method='POST', data={'year': '2022', 'month': '12', 'day': '31', 'price_class': 'SE3'}):
    #     response = urllib.request(f"https://www.elprisetjustnu.se/api/v1/prices/{2022}/{12}-{31}_{SE3}.json")
        assert response.status_code == 200
        assert b'Resultat' in response.headline
        

def test_catch_404():
    with urllib.request("http://127.0.0.1:5000/log", context=context, timeout=10) as response:
        html = str(response.read())
        assert "404" not in html

#TODO: testcase för post på api
#TODO: testcase att se att data för visst datumn stämmer
#TODO: göra testcase för funktionerna i app.py
