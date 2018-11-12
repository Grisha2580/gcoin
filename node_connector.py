# This file represents a node connector, whose responsibility is to connect nodes by giving them the addresses
# of each other.

print('This is the name {}'.format(__name__))
from flask import Flask, jsonify, request
import sys
import json
from argparse import ArgumentParser
import requests

app = Flask(__name__)

"""
    This class is the connector, who behaves like a main server, who has all the information about the nodes.
    Has one attribute:
    :param nodes - dict, where key is the unique id of the node and value is a tuple with address and port.
    """

nodes = {}
address = None
port = None


@app.route('/add', methods=['POST'])
def add_node():
    """
    Adds the node to the dictionary.
    """
    global nodes
    message = request.data
    node = json.loads(message)
    print(node)

    node_id = node['id']
    node_address = node['address']
    node_port = node['port']

    if node_id in nodes.keys() or (node_address, node_port) in nodes.values():
        return 'Node already exist', 409
    else:

        update_nodes('peers', node)
        nodes[node_id] = (node_address, node_port)
        print('Now the nodes are {}'.format(nodes))
        print('A new node has joined the network {}'.format(node_id))
        return 'Successfully added node to the P2P server', 200


def update_nodes(url, message):
    for key, value in nodes.items():
        requests.post('http://{}:{}/{}'.format(value[0], value[1], url), data=json.dumps(message))


@app.route('/get', methods=['GET'])
def get_nodes():
    """
    Responds with all the nodes the networks has currently.
    :return:
    """

    return jsonify(nodes), 200


if __name__ == '__main__':
    print('This is standard output', file=sys.stdout)
    if len(sys.argv) >= 3:
        address = sys.argv[1]
        port = sys.argv[2]
    else:
        print("Illegal argument, cant start the node")
        sys.exit(0)

    app.run(host=address, port=port)
