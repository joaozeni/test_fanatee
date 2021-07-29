import csv
from collections import defaultdict
from heapq import *

from flask import Blueprint, request, jsonify
from sqlalchemy.dialects.postgresql import insert

from apis.models.vertex import vertex
from apis.models.model import db


paths_blueprint = Blueprint('paths', __name__)


@paths_blueprint.route('/insert_map', methods=['POST'])
def insert_map():
    """Insert or update a path to the system
        ---
        parameters:
            - name: map
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
    paths_file = request.files.get('map')
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


@paths_blueprint.route('/search_path', methods=['GET'])
def search_path():
    """Search fot the best path
        ---
        parameters:
            - name: origin
              in: query
              type: string
              required: true
            - name: destiny
              in: query
              type: string
              required: true
        responses:
          200:
            description: returns a json with cost and path, the path is an ordenated array
          204:
            description: when thre is no path betweem origin and destiny
          400:
            description: returns MISSING_PARAMETER if the parameters are not sent
    """
    req_args = request.args
    if not req_args or not req_args.get('origin') or not req_args.get('destiny'):
        return {'message':'MISSING_PARAMETER'}, 400
    
    origin = req_args.get('origin')
    destiny = req_args.get('destiny')
    
    vertex_query = db.session.query(vertex).all()
    
    graph = defaultdict(list)
    for vertex_obj in vertex_query:
        graph[vertex_obj.origin].append((vertex_obj.cost, vertex_obj.destiny))

    q, seen, dist = [(0,origin,())], set(), {origin: 0}
    while q:
        (cost,current_node,path) = heappop(q)
        if current_node in seen:
            continue
        seen.add(current_node)
        path += (current_node,)
        if current_node == destiny: 
            return {'cost': cost, 'path': path}, 200

        for cost_current_neighbor, neighbor_node in graph.get(current_node, ()):
            if neighbor_node in seen:
                continue
            # Not every edge will be calculated. The edge which can improve the value of node in heap will be useful.
            if neighbor_node not in dist or cost+cost_current_neighbor < dist[neighbor_node]:
                dist[neighbor_node] = cost+cost_current_neighbor
                heappush(q, (cost+cost_current_neighbor, neighbor_node, path))
    
    return 'NO_PATH', 204

