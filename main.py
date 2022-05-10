import json
import random
import sys
import time
from threading import RLock, Thread, Timer

import zmq

WAIT_TIME_TO_CONNECT_PEERS = 5


# https://stackoverflow.com/a/56169014
class ResettableTimer:
    def __init__(self, function, interval_lb=100, interval_ub=200):
        self.interval = (interval_lb, interval_ub)
        self.function = function
        self.timer = Timer(self._interval(), self.function)

    def _interval(self):
        return random.randint(*self.interval)

    def run(self):
        self.timer.start()

    def reset(self):
        self.timer.cancel()
        self.timer = Timer(self._interval(), self.function)
        self.timer.start()


class Sender:
    def __init__(self, port, peers, context):
        self.my_id = port.encode()
        self.socket = context.socket(zmq.ROUTER)
        self.socket.setsockopt(zmq.IDENTITY, self.my_id)
        self.reentrant_lock = RLock()

        self.peer_ids = []
        for ip, port in peers:
            self.peer_ids.append(port.encode())
            self.socket.connect(f"tcp://{ip}:{port}")
        # give time to actually connect
        time.sleep(WAIT_TIME_TO_CONNECT_PEERS)

    def broadcast_to_peers(self, message):
        for peer_id in self.peer_ids:
            print(self.my_id, "sending a message to", peer_id)
            self.send_to_peer(peer_id, message.encode())
        print(self.my_id, "sent all messages")

    def send_to_peer(self, peer_id, message):
        self.reentrant_lock.acquire()
        self.socket.send_multipart([peer_id, message.encode()])
        self.reentrant_lock.release()


class Receiver:
    def __init__(self, ip, port, context):
        self.my_id = port.encode()
        self.socket = context.socket(zmq.ROUTER)
        self.socket.setsockopt(zmq.IDENTITY, port.encode())
        self.socket.bind(f"tcp://{ip}:{port}")
        self.reentrant_lock = RLock()
        self.thread = Thread(target=self.start_receiving)
        self.thread.start()

    def start_receiving(self):
        while True:
            self.reentrant_lock.acquire()
            sender_id, sender_message = self.socket.recv_multipart()
            self.reentrant_lock.release()

            print(
                self.my_id,
                " server received: ",
                sender_message.decode(),
                " from: ",
                sender_id.decode(),
            )

    def __del__(self):
        self.thread.join(100)


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


def main(my_ip, my_port, peers):
    context = zmq.Context()
    sender = Sender(my_port, peers, context)
    receiver = Receiver(my_ip, my_port, context)
    print("created sender/receiver")
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
