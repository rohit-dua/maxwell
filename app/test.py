from app import app, db
import tempfile
import pytest
import os
import configparser
import utils
import json

configini = configparser.ConfigParser()
configini.read(utils.envConfigFile())

def json_of_response(response):
    """Decode json from response"""
    return json.loads(response.data.decode('utf8'))

token = None
listId = None

@pytest.fixture(scope="session")
def client():
    app.config['SQLALCHEMY_DATABASE_URI'] = configini['TEST']['database_uri']
    app.config['TESTING'] = True
    app.app_context().push()
    db.init_app(app)
    db.create_all()
    client = app.test_client()
    yield client
    os.unlink(app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///',''))

@pytest.mark.run(order=1)
def test_200(client):
    """200 ack test"""
    resp = client.get('/')
    assert resp.status_code == 200

@pytest.mark.run(order=2)
def test_register(client):
    resp = client.post('/register', data=json.dumps(dict(username='test', password='test')), content_type='application/json')
    assert json_of_response(resp)[u'status'] == 'success'

@pytest.mark.run(order=3)
def test_get_token(client):
    global token
    resp = client.post('/fetchAccessToken', data=json.dumps(dict(username='test', password='test')), content_type='application/json')
    token = json_of_response(resp)[u'token']
    assert json_of_response(resp)[u'status'] == 'success'

@pytest.mark.run(order=4)
def test_addList(client):
    global token, listId
    resp = client.post('/addList', data=json.dumps(dict(listName='testList', token=token)), content_type='application/json')
    listId = json_of_response(resp)['id']
    assert json_of_response(resp)[u'status'] == 'success'

@pytest.mark.run(order=5)
def test_addItem(client):
    global token, listId
    resp = client.post('/addItem', data=json.dumps(dict(listId=listId, token=token, item="test")), content_type='application/json')
    assert json_of_response(resp)[u'status'] == 'success'
