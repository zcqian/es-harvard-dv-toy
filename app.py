import json

from typing import List
from elasticsearch import Elasticsearch
import elasticsearch.exceptions


from flask import Flask, request, jsonify, abort

app = Flask(__name__)

es = Elasticsearch(hosts=["192.168.21.136"])


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/setup', methods=['POST', 'DELETE'])
def index_setup():
    # default reply, we will let the app crash if this fails
    success = {'success': True}

    # setup the index and custom mapping
    if request.method == 'POST':
        if es.indices.exists(index='dv'):
            abort(400)
        es.indices.create(index='dv', body={
            'settings': {'analysis': {'normalizer': {'ci_folding_norm': {'type': 'custom', 'char_filter': [], 'filter': ['lowercase', 'asciifolding']}}}},
            'mappings': {'properties': {'funder.name': {'type': 'text', 'fields': {'keyword_ci': {'type': 'keyword', 'normalizer': 'ci_folding_norm'}}}}}
        })
    # drop the index
    elif request.method == 'DELETE':
        if es.indices.exists(index='dv'):
            es.indices.delete(index='dv')
    # default, do nothing
    else:
        pass
    # return success
    return jsonify(success), 200


# TODO: refactor this part
@app.route('/data', methods=['POST', 'GET', 'DELETE'])
def handle_data():
    success = {'success': True}
    if request.method == 'POST':
        d = request.get_json()
        if isinstance(d, dict):
            app.logger.debug("Insert single document")
            insert_data([d])
            return jsonify(success)
        elif isinstance(d, list):
            app.logger.debug("Insert multi document")
            insert_data(d)
            return jsonify(success)
        else:
            abort(400)
    elif request.method == 'GET':
        idx = request.args.get('id', None, type=str)
        if idx:
            try:
                source = es.get_source(index='dv', id=idx)
                code = 200
            except elasticsearch.exceptions.NotFoundError:
                source = {}
                code = 400
            return jsonify(source), code
        else:
            return jsonify({}), 404
    elif request.method == 'DELETE':
        es.delete_by_query(index='dv', body={"query": {"match_all": {}}})
        return jsonify(success)
    else:
        abort(400)


@app.route('/search', methods=['GET'])
def search_data():
    # TODO: implement searching
    abort(500)


def insert_data(data: List[dict]):
    """ insert data into Elastic Search index

    :param data: list of data in dictionaries, decoded from JSON
    :return: None
    """
    for item in data:
        # I assume that @id is unique
        # nobody said it is guaranteed to be unique, but it makes sense
        es.create(index='dv', id=item['@id'], body=item)


if __name__ == '__main__':
    app.run()
