import json
import sys

from logg import debug_print
from raft import Node
from zmq_comms import ZMQSender, ZMQReceiver


def parse_config_json(fp, idx):
    config_json = json.load(open(fp))

    my_ip, my_port = None, None
    peers = []
    for i, address in enumerate(config_json["addresses"]):
        ip, port = address["ip"], address["port"]
        if i == idx:
            my_ip, my_port = ip, port
        else:
            peers.append((ip, port))

    return my_ip, my_port, peers


def main(my_ip, my_port, peers):
    sender = ZMQSender(my_port, peers)
    node = Node(my_port, sender.broadcast_dict_to_peers)
    receiver = ZMQReceiver(my_ip, my_port, node.rpc_handler)
    debug_print("created sender/receiver")
    receiver.join()


if __name__ == "__main__":
    config_json_fp = sys.argv[1]
    config_json_idx = int(sys.argv[2])
    my_ip, my_port, peers = parse_config_json(config_json_fp, config_json_idx)
    debug_print(my_ip, my_port, peers)
    main(my_ip, my_port, peers)
