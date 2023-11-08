import pytest
import urllib.request
import ssl
import flask
from application.app import app
import json
from application import func
import pandas as pd
from io import StringIO


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


def test_respone_to_df():
    """
    Testar om funktion respone_to_df returnerar en pandas dataframe
    """
    fake_response = [{
        "SEK_per_kWh": 0.02218,
        "EUR_per_kWh": 0.002,
        "EXR": 11.091763,
        "time_start": "2022-12-31T00:00:00+01:00",
        "time_end": "2022-12-31T01:00:00+01:00"
    }]
    fake_response = json.dumps(fake_response)
    # gör om fake_response till en StringIO som är en fil som simulerar api svaret, detta gör att vi kan köra .read() på den
    fake_response = StringIO(fake_response)
    response_to_df = func.respone_to_df(fake_response)
    assert isinstance(response_to_df, pd.DataFrame)


def test_rename_dr():
    """
    testar om rename_dr byter namn på kolumnerna i en dataframe
    """
    # skapar en dataframe
    df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})

    # skapar en dictionary med key som är det nuvarande namnet på kolumnen och value som är det nya namnet på kolumnen
    rename_dict = {'A': 'new_A', 'B': 'new_B'}

    # anropar rename_dr
    func.rename_dr(df, rename_dict)

    # listar kolumnerna i dataframen och kollar om de nya namnen finns med
    assert list(df.columns) == ['new_A', 'new_B']


def test_extract_date_from_dataframe():
    """
    testar om funktionen extract_date_from_dataframe returnerar rätt datum
    """
    # skapar en dataframe
    df = pd.DataFrame({
        'time_start': ['2022-01-01T10:00:00', '2022-01-02T11:00:00', '2022-01-03T12:00:00']})

    # kallar på extract_date_from_dataframe
    date = func.extract_date_from_dataframe(df)

    # kollar om datumet är korrekt
    assert date == '2022-01-01'


def test_create_time_column():
    """
    testar om create_time_column skapar en ny kolumn med tid utan sekunder och tar bort time_start, time_end och EXR
    """
    # skpar en dataframe
    df = pd.DataFrame({
        'time_start': ['2022-01-01T12:34:56+00:00', '2022-01-01T23:59:59+00:00'],
        'time_end': ['2022-01-01T13:00:00+00:00', '2022-01-02T00:00:00+00:00'],
        'EXR': ['foo', 'bar']
    })

    # anropar funktionen
    result = func.create_time_column(df)

    # kollar om kolumnen 'Tid' finns med i dataframen
    assert 'Tid' in result.columns

    # gör om kolumnen tid till en lista och kontrollerar om tiderna är korrekta
    assert result['Tid'].tolist() == ['12:34', '23:59']

    # kontrollerar att time_start, time_end och EXR inte finns med i dataframen
    assert 'time_start' not in result.columns
    assert 'time_end' not in result.columns
    assert 'EXR' not in result.columns


def test_df_to_html():
    """
    testar om df_to_html returnerar en sträng som innehåller en html tabell
    """
    # skapar en dataframe
    df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
    # anropar funktionen
    result = func.df_to_html(df)
    # kontrollerar att resultatet är en sträng
    assert isinstance(result, str)
    # kontrollerar att resultatet innehåller en html tabell
    assert '<th>col1</th>' in result
    assert '<th>col2</th>' in result
    # kontrollerar att resultatet innehåller rätt värden
    assert '<td>1</td>' in result
    assert '<td>2</td>' in result
    assert '<td>3</td>' in result
    assert '<td>4</td>' in result

def no_error_on_404():
    client = app.test_client()
    response = client.get('/sida_som_inte_finns')
    assert response.status_code == 200
    assert 'Sidan du söker finns inte'.encode('utf-8') in response.data
