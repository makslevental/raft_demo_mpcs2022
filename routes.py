from flask import Flask, request, jsonify

from raft import Node

app = Flask(__name__)

raft_node: Node = None


@app.route("/request-vote/<id>", methods=["POST"])
def request_vote(id):
    rpc_message_json = request.json
    res = raft_node.rpc_handler(id, rpc_message_json)
    return jsonify(res)
