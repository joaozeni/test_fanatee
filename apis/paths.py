import csv

from flask import Blueprint, request, jsonify
from sqlalchemy.dialects.postgresql import insert

from apis.models.vertex import vertex
from apis.models.model import db


paths_blueprint = Blueprint('paths', __name__)


@paths_blueprint.route('/insert_path', methods=['POST'])
def insert_path():
    """Insert or update a path to the system
        ---
        parameters:
            - name: paths
              in: formData
              type: file
              required: true
        responses:
          201:
            description: returns OK if the paths were correctly inserted
          400:
            description: returns NO_FILE if the was not sent
          400:
            description: returns WRONG_FORMAT if the sent file is not decodable or in not in csv specified
    """
    paths_file = request.files.get('paths')
    if not paths_file:
        return {'message': 'NO_FILE'}, 400
    
    try:
        csv_reader = csv.reader(paths_file.read().decode("utf-8").splitlines(), delimiter=',')
    except:
        return {'message': 'WRONG_FORMAT'}, 400
    
    insert_stmt = insert(vertex)

    insert_dicts = []
    for row in csv_reader:
        try:
            insert_dicts.append({'origin':row[0], 'destiny':row[1], 'cost':int(row[2])})
        except:
            return {'message': 'WRONG_FORMAT'}, 400

    insert_stmt = insert_stmt.values(insert_dicts).on_conflict_do_nothing(index_elements=['origin', 'destiny'])

    db.session.execute(insert_stmt)
    db.session.commit()
    
    return {'message':'OK'}, 201

