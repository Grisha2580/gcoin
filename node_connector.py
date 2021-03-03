# This file represents a node connector, whose responsibility is to connect nodes by giving them the addresses
# of each other.

print('This is the name {}'.format(__name__))
from flask import Flask, jsonify, request
import sys
import json
import requests
from util import hash_it

app = Flask(__name__)

"""
This class is the connector, who behaves like a main server, who has all the information about the nodes.
Has one attribute:
:param nodes - dict, where key is the unique id of the models and value is a tuple with address and port.
:param address - the ip address of the connector (by default should be 127.0.0.1)
:param port = the port of the connector (by default 5000)
"""

nodes_addresses = {}
nodes_public_keys = {}
address = None
port = None





@app.route('/nodes', methods=['POST', 'GET'])
def add_node():
    """
    Adds the models to the dictionary.
    """
    global nodes_addresses
    global nodes_public_keys
    if request.method == 'GET':
        return jsonify(nodes_addresses), 200


    message = request.data
    node = json.loads(message)
    print(node)

    node_id = node['id']
    node_address = node['address']
    node_port = node['port']
    node_public_key = node['public_key']


    if node_id in nodes_addresses.keys() or (node_address, node_port) in nodes_addresses.values():

        return 'Node already exist', 409
    else:
        del node['public_key']
        update_nodes('peers', node)
        nodes_addresses[node_id] = (node_address, node_port)
        nodes_public_keys[node_id] = node_public_key

        return 'Successfully added node to the P2P server', 200


def update_nodes(url, message):
    """
    Sends the given message to all the nodes the connector knows of.
    :param url: the url of where exactly it should post.
    :param message: JSON, representing the message to send.
    """
    for key, value in nodes_addresses.items():
        requests.post('http://{}:{}/{}'.format(value[0], value[1], url), data=json.dumps(message))


@app.route('/nodes/address/<id>', methods=['GET'])
def get_node_address(id):
    """
    Responds with all the nodes the networks has currently.
    :return:
    """

    node_public_key = nodes_public_keys[id]
    try:
        node_address = hash_it(node_public_key)
        return jsonify(node_address), 200
    except:
        return 'No node with such id in the database', 409


def get_node_public_address():
    pass


if __name__ == '__main__':
    print('This is standard output', file=sys.stdout)
    if len(sys.argv) >= 3:
        address = sys.argv[1]
        port = sys.argv[2]
    else:
        print("Illegal argument, cant start the models")
        sys.exit(0)

    app.run(host=address, port=port)
