import pytest
import urllib.request
import ssl
import flask
from application.app import app
import json


context = ssl._create_unverified_context()


def test_Is_online_index():
    """
    Denna funktion testar om servern är online genom att göra ett anrop mot endpoint '/'.
    """
    assert urllib.request.urlopen(
        "http://127.0.0.1:5000", context=context, timeout=10)


def test_Is_online_form():
    """
    Denna funktion testar om servern är online genom att göra ett anrop mot endpoint '/form'.
    """
    assert urllib.request.urlopen(
        "http://127.0.0.1:5000/form", context=context, timeout=10)


def test_Confirm_HTTPError_on_api_GET():
    """
    testar att get request till endpoint '/api' ger en HTTPError
    """
    with pytest.raises(urllib.request.HTTPError):
        urllib.request.urlopen("http://127.0.0.1:5000/api",
                               context=context, timeout=10)


def test_api_return_correct_data():
    """
    Detta testar om en av de nestlade dictionaries i listan som returneras från API:et finns in api svaret vilket betyder att svaret är korrekt
    då det innehåller datumet som skickades med i anropet.
    """
    expected_data = {
        "SEK_per_kWh": 0.02218,
        "EUR_per_kWh": 0.002,
        "EXR": 11.091763,
        "time_start": "2022-12-31T00:00:00+01:00",
        "time_end": "2022-12-31T01:00:00+01:00"
    }

    api_response = urllib.request.urlopen(
        "https://www.elprisetjustnu.se/api/v1/prices/2022/12-31_SE3.json")
    api_data_bytes = api_response.read()
    api_data_str = api_data_bytes.decode('utf-8')  # Convert bytes to string
    # Parse JSON data into a dictionary
    response_api_data = json.loads(api_data_str)

    # Now, you need to find the correct way to compare expected_data with response_api_data.
    # This depends on how the API formats its response.
    # If it returns an array of objects and you need to check if one of those objects matches expected_data:
    assert expected_data in response_api_data


def no_error_on_404():
    client = app.test_client()
    response = client.get('/sida_som_inte_finns')
    assert response.status_code == 200
    assert 'Sidan du söker finns inte'.encode('utf-8') in response.data
