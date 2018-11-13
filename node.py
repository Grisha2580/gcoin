# This file represents a node in the P2P network.

from flask import Flask, render_template, request, jsonify
from blockchain import Blockchain
import json
from util import get_address, convert_to_transaction

from miner import Miner
import requests
import sys
import hashlib
from transaction import Transaction
from wallet import Wallet

app = Flask(__name__)

"""
This file represents one node in the P2P network.
Has 5 attributes:
:param blockchain - Blockchain object, which represents the current blockchain.
:param miner - Miner object, which helps the node mine if it wants.
:param neighbors - all the neighbors the node share its infromation to the in the P2P network.
:param address - the address the node is running on.
:param the port the node is running on.
"""

id = None
blockchain = Blockchain()
miner = None
neighbors = None
connector = ('127.0.0.1', '5000')
wallet = None
address = None
port = None


def collect_neighbors():
    """
    This function searches for the peers in the network.
    """
    global neighbors
    response = requests.get('http://{}:{}/get'.format(connector[0], connector[1]))
    if response.status_code == 200:
        peers = response.json()
        print("Node {} now has the following neighbors {}".format(id, peers))
        neighbors = peers

    else:
        print('Could not get neighbors, something has happened to the server')


def self_register():
    """
    This function is registering the node in the network.
    """
    message = {'id': id, 'address': address, 'port': port}
    response = requests.post("http://{}:{}/add".format(connector[0], connector[1]), data=json.dumps(message))

    if response.status_code == 200:
        print("{}: Successfully registered".format(id))


@app.route('/peers', methods=['POST'])
def add_neighbor():
    """
    Adds a new neighbor to the current peer.
    :return:
    """
    global neighbors
    new_peer = json.loads(request.data)
    peer_id = new_peer['id']
    peer_address = new_peer['address']
    peer_port = new_peer['port']

    neighbors[peer_id] = (peer_address, peer_port)
    print('Now my peers are {}'.format(neighbors))

    return "Successfully added new peer", 200

def get_updated():
    """
    Checks if somebody in the peers has a better blockchain
    :return: 
    """
    global blockchain
    best_blockchain = blockchain
    for key, value in neighbors.items():
        node_destination = get_address(value[0], value[1])
        response = requests.get(node_destination + '/blockchain/get')

        if response.status_code == 200:
            peer_blockchain = Blockchain(response.json())

            if peer_blockchain.check_blockchain() and peer_blockchain.size() > best_blockchain.size():
                best_blockchain = peer_blockchain

    print('My blockchain size is now {}'.format(blockchain.size()))

@app.route('/blockchain/get', methods=['GET'])
def get_blockchain():
    json_chain = blockchain.to_json()
    print('Somebody has asked for my blockchain')

    return jsonify(json_chain), 200


@app.route('/blockchain/post', methods=['POST'])
def post_blockchain():
    global blockchain
    posted_blockchain = json.loads(request.data)
    print('This is what I got {}'.format(posted_blockchain))
    new_blockchain = Blockchain(posted_blockchain)
    print("{}: Demand to change my blockchain".format(request))
    valid_blockchain = new_blockchain.check_blockchain()
    longer_blockchain = new_blockchain.size() > blockchain.size()
    print("The validity of the blockchain {}".format(valid_blockchain))
    print("The blockchain is longer than mine {}".format(longer_blockchain))
    if longer_blockchain and valid_blockchain:
        blockchain = new_blockchain

        return "The blockchain has been updated", 201
    else:
        message = {'message': 'Your blockchain is either invalid or smaller than mine',
                   'blockchain': blockchain.to_json()}

        print('My blockchain size is now {}'.format(blockchain.size()))

        return jsonify(message), 409

@app.route('/transactions/update', methods=['POST'])
def transactions_update():
    """
    This request updates the node transaction pool, but does not spread the transaction among the network.
    This request happens automatically and is not being done by the user.
    """

    posted_transaction = json.loads(request.data)

    transaction = convert_to_transaction(posted_transaction)

    if transaction.verify():
        blockchain.add_transaction(transaction)

        return "Transaction was successfully submitted", 201

    else:
        return "The transaction is not valid", 200



@app.route('/transactions/post', methods=['POST'])
def post_transaction():
    """
    Spread the transaction among the network. This request is done by the user of the blockchain.
    :return:
    """
    global blockchain
    address = request.args.get('address')
    value = request.args.get('value')

    transaction = wallet.pay(address, value)

    try:
        blockchain.add_transaction(transaction)
        for key, value in neighbors.items():
            node_destination = get_address(value[0], value[1])
            requests.post(node_destination + '/transactions/update', data=json.dumps(transaction))

        return "Transaction was submitted", 201
    except:
        return "The transaction is invalid", 409




@app.route('/blockchain/mine', methods=['GET'])
def run_miner():
    global blockchain
    """
    Any node in the network can become a miner and start mining blocks.
    :return:
    """
    miner = Miner(blockchain, id)
    new_block = miner.run_mining()
    blockchain.add_block(new_block)
    print("{} node has mined a new block".format(id))
    print('New size of the blockchain is {}'.format(blockchain.size()))

    for key, value in neighbors.items():
        address = 'http://{}:{}/blockchain/post'.format(value[0], value[1])
        # send the new chain to all the miners
        print("sending ")
        requests.post(address, data=json.dumps(blockchain.to_json()))

    return 'The block was created', 200


if __name__ == '__main__':
    if len(sys.argv) >= 4:
        address = sys.argv[1]
        port = sys.argv[2]
        id = sys.argv[3]
    else:
        print("Illegal argument, cant start the node")
        sys.exit(0)

    collect_neighbors()
    self_register()
    get_updated()
    blockchain.mine_genesis()
    wallet = Wallet(blockchain)
    app.run(host=address, port=port)
