import pytest
from io import BytesIO
from flask_migrate import Migrate

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__),'../'))

from apis.app import create_app
from apis.models.model import db
from apis.models.vertex import vertex


@pytest.fixture(scope="module")
def app():
    app = create_app(test_config=True)

    with app.app_context():
        db.create_all()
        Migrate(app, db)
    
    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()

def test_insert_clean_db(app):
    data = {'paths':(BytesIO(b'TER,MAR,10\rMAR,LUA,5'), "exemplo.csv")}
    result = app.test_client().post('/paths/insert_path', content_type='multipart/form-data', data=data)
    assert result.get_json().get('message') == 'OK'
    assert result.status_code == 201
    with app.app_context():
        query = db.session.query(vertex)
        query_results = db.session.execute(query).all()
        assert len(query_results) == 2
        assert query_results[0][0].origin == 'TER'
        assert query_results[0][0].destiny == 'MAR'
        assert query_results[0][0].cost == 10
        assert query_results[1][0].origin == 'MAR'
        assert query_results[1][0].destiny == 'LUA'
        assert query_results[1][0].cost == 5

def test_insert_file_not_send(app):
    data = {'paths':(BytesIO(b'TER,MAR,10\rMAR,LUA,5'), "exemplo.csv")}
    result = app.test_client().post('/paths/insert_path', content_type='multipart/form-data')
    assert result.get_json().get('message') == 'NO_FILE'
    assert result.status_code == 400

def test_insert_wrong_format(app):
    data = {'paths':(BytesIO(b'abcqwerty'), "exemplo.csv")}
    result = app.test_client().post('/paths/insert_path', content_type='multipart/form-data', data=data)
    assert result.get_json().get('message') == 'WRONG_FORMAT'
    assert result.status_code == 400

def test_upsert(app):
    data = {'paths':(BytesIO(b'TER,PLU,75\rTER,LUA,20'), "exemplo.csv")}
    result = app.test_client().post('/paths/insert_path', content_type='multipart/form-data', data=data)
    assert result.get_json().get('message') == 'OK'
    assert result.status_code == 201
    with app.app_context():
        query = db.session.query(vertex)
        query_results = db.session.execute(query).all()
        assert len(query_results) == 4
        assert query_results[0][0].origin == 'TER'
        assert query_results[0][0].destiny == 'MAR'
        assert query_results[0][0].cost == 10
        assert query_results[1][0].origin == 'MAR'
        assert query_results[1][0].destiny == 'LUA'
        assert query_results[1][0].cost == 5
        assert query_results[2][0].origin == 'TER'
        assert query_results[2][0].destiny == 'PLU'
        assert query_results[2][0].cost == 75
        assert query_results[3][0].origin == 'TER'
        assert query_results[3][0].destiny == 'LUA'
        assert query_results[3][0].cost == 20

def test_upsert_repeated(app):
    data = {'paths':(BytesIO(b'TER,MAR,10\rTER,LUA,20'), "exemplo.csv")}
    result = app.test_client().post('/paths/insert_path', content_type='multipart/form-data', data=data)
    assert result.get_json().get('message') == 'OK'
    assert result.status_code == 201
    with app.app_context():
        query = db.session.query(vertex)
        query_results = db.session.execute(query).all()
        assert len(query_results) == 4
        assert query_results[0][0].origin == 'TER'
        assert query_results[0][0].destiny == 'MAR'
        assert query_results[0][0].cost == 10
        assert query_results[1][0].origin == 'MAR'
        assert query_results[1][0].destiny == 'LUA'
        assert query_results[1][0].cost == 5
        assert query_results[2][0].origin == 'TER'
        assert query_results[2][0].destiny == 'PLU'
        assert query_results[2][0].cost == 75
        assert query_results[3][0].origin == 'TER'
        assert query_results[3][0].destiny == 'LUA'
        assert query_results[3][0].cost == 20

def test_upsert_repeated_and_new(app):
    data = {'paths':(BytesIO(b'TER,LUA,20\rTER,NET,56'), "exemplo.csv")}
    result = app.test_client().post('/paths/insert_path', content_type='multipart/form-data', data=data)
    assert result.get_json().get('message') == 'OK'
    assert result.status_code == 201
    with app.app_context():
        query = db.session.query(vertex)
        query_results = db.session.execute(query).all()
        assert len(query_results) == 5
        assert query_results[0][0].origin == 'TER'
        assert query_results[0][0].destiny == 'MAR'
        assert query_results[0][0].cost == 10
        assert query_results[1][0].origin == 'MAR'
        assert query_results[1][0].destiny == 'LUA'
        assert query_results[1][0].cost == 5
        assert query_results[2][0].origin == 'TER'
        assert query_results[2][0].destiny == 'PLU'
        assert query_results[2][0].cost == 75
        assert query_results[3][0].origin == 'TER'
        assert query_results[3][0].destiny == 'LUA'
        assert query_results[3][0].cost == 20
        assert query_results[4][0].origin == 'TER'
        assert query_results[4][0].destiny == 'NET'
        assert query_results[4][0].cost == 56

