import json
import sys

from logg import logger, debug_print
from raft import Node
from zmq_comms import ZMQSender, ZMQReceiver


def parse_config_json(fp, idx):
    config_json = json.load(open(fp))

    my_ip, my_port = None, None
    peers = []
    for i, address in enumerate(config_json["addresses"]):
        ip, port = address["ip"], str(address["port"])
        if i == idx:
            my_ip, my_port = ip, port
        else:
            peers.append((ip, port))

    return my_ip, my_port, peers


def receive_handler(sender_id, sender_message):
    debug_print(
        " server received: ",
        sender_message,
        " from: ",
        sender_id,
    )


def main(my_ip, my_port, peers):
    node = Node(my_port, [port for _, port in peers])
    sender = ZMQSender(my_port, peers)
    receiver = ZMQReceiver(my_ip, my_port, node.rpc_handler)
    debug_print("created sender/receiver")
    if my_port == "46781":
        sender.send_to_peer("46782".encode(), "hello")
    elif my_port == "46782":
        sender.send_to_peer("46781".encode(), "world")


if __name__ == "__main__":
    config_json_fp = sys.argv[1]
    config_json_idx = int(sys.argv[2])
    my_ip, my_port, peers = parse_config_json(config_json_fp, config_json_idx)
    # print(my_ip, my_port, peers)

    main(my_ip, my_port, peers)
