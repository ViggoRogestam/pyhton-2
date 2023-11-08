# import pytest
# from application.app import app

# @pytest.fixture
# def client():
#     with app.test_client() as client:
#         yield client

# def test_index_route(client):
#     """Test the index route."""
#     response = client.get('/')
#     assert response.status_code == 200
#     assert b'index' in response.data

# def test_form_route(client):
#     """Test the form route."""
#     response = client.get('/form')
#     assert response.status_code == 200
#     expected_respone ='<p>Ange datum och prisklass för att se elpriser.<br>Datumet får inte vara före 2022-11-01 och inte längre fram i tiden än 1 dag fram i tiden</p>' in response.data
#     assert expected_respone.encode('utf-8') in response.data
# def test_api_route(client):
#     """Test the /api route with POST method."""
#     # You'll need to send through form data to this route
#     # Here's an example of what that might look like:
#     test_data = {
#         'year': '2021',
#         'month': '01',
#         'day': '01',
#         'price_class': 'some_price_class'
#     }
#     response = client.post('/api', data=test_data)
#     assert response.status_code == 200
#     # Add additional assertions relevant to your application

# def test_404_error(client):
#     """Test a 404 error."""
#     response = client.get('/nonexistentpath')
#     assert response.status_code == 404
#     expected_respone = 'Sidan du söker finns inte'
#     assert expected_respone.encode('utf-8') in response.data
