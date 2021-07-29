import pytest
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

def test_search_with_just_one_vertex(app):
    with app.app_context():
        vertex_obj = vertex(origin='TER', destiny='MAR', cost=10)
        db.session.add(vertex_obj)
        db.session.commit()
    result = app.test_client().get('/paths/search_path?origin=TER&destiny=MAR')
    assert result.get_json().get('cost') == 10
    assert result.get_json().get('path') == ['TER', 'MAR']

def test_search_with_two_vertex(app):
    with app.app_context():
        vertex_obj = vertex(origin='MAR', destiny='LUA', cost=5)
        db.session.add(vertex_obj)
        db.session.commit()
    result = app.test_client().get('/paths/search_path?origin=TER&destiny=LUA')
    assert result.get_json().get('cost') == 15
    assert result.get_json().get('path') == ['TER', 'MAR', 'LUA']

def test_search_with_three_vertex_hooping(app):
    with app.app_context():
        vertex_obj = vertex(origin='TER', destiny='LUA', cost=10)
        db.session.add(vertex_obj)
        db.session.commit()
    result = app.test_client().get('/paths/search_path?origin=TER&destiny=LUA')
    assert result.get_json().get('cost') == 10
    assert result.get_json().get('path') == ['TER', 'LUA']

def test_search_with_three_vertex_bigger_direct(app):
    with app.app_context():
        vertex_obj = vertex.query.filter_by(origin='TER').filter_by(destiny='LUA').first()
        vertex_obj.cost = 20
        db.session.commit()
    result = app.test_client().get('/paths/search_path?origin=TER&destiny=LUA')
    assert result.get_json().get('cost') == 15
    assert result.get_json().get('path') == ['TER', 'MAR', 'LUA']

def test_search_full_graph_ex1(app):
    with app.app_context():
        vertex_obj1 = vertex(origin='TER', destiny='PLU', cost=75)
        vertex_obj2 = vertex(origin='TER', destiny='NET', cost=56)
        vertex_obj3 = vertex(origin='NET', destiny='PLU', cost=5)
        vertex_obj4 = vertex(origin='LUA', destiny='NET', cost=20)
        vertex_obj5 = vertex(origin='LUA', destiny='PLU', cost=11)
        db.session.add(vertex_obj1)
        db.session.add(vertex_obj2)
        db.session.add(vertex_obj3)
        db.session.add(vertex_obj4)
        db.session.add(vertex_obj5)
        db.session.commit()
    result = app.test_client().get('/paths/search_path?origin=TER&destiny=PLU')
    assert result.get_json().get('cost') == 26
    assert result.get_json().get('path') == ['TER', 'MAR', 'LUA', 'PLU']

def test_search_full_graph_ex2(app):
    result = app.test_client().get('/paths/search_path?origin=MAR&destiny=PLU')
    assert result.get_json().get('cost') == 16
    assert result.get_json().get('path') == ['MAR', 'LUA', 'PLU']

def test_search_not_send_origin(app):
    result = app.test_client().get('/paths/search_path?destiny=PLU')
    assert result.status_code == 400
    assert result.get_json().get('message') == 'MISSING_PARAMETER'

def test_search_not_send_destiny(app):
    result = app.test_client().get('/paths/search_path?origin=PLU')
    assert result.status_code == 400
    assert result.get_json().get('message') == 'MISSING_PARAMETER'

def test_search_not_send_params(app):
    result = app.test_client().get('/paths/search_path')
    assert result.status_code == 400
    assert result.get_json().get('message') == 'MISSING_PARAMETER'

def test_search_no_path(app):
    result = app.test_client().get('/paths/search_path?origin=MAR&destiny=VEN')
    assert result.status_code == 204

