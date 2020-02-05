import json

from typing import List

from flask import Flask, request, jsonify, abort

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


# TODO: set up proper mapping for data
@app.route('/data', methods=['POST', 'GET'])
def handle_data():
    if request.method == 'POST':
        d = request.get_json()
        if isinstance(d, dict):
            insert_data([d])
        elif isinstance(d, list):
            insert_data(d)
        else:
            abort(400)
    elif request.method == 'GET':
        # TODO: implement getting single item
        pass

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
    pass

if __name__ == '__main__':
    app.run()
