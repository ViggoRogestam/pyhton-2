from application import app

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
        
#TODO: testa connection till alla routes
#TODO: testa att api returnerar rätt data
#TODO: testa att api returnerar rätt statuskod
#TODO: testa att bara post funkar på api
