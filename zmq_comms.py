import json
import time
from threading import RLock, Thread

import zmq

from logg import debug_print

WAIT_TIME_TO_CONNECT_PEERS = 1
context = zmq.Context()


class ZMQSender:
    def __init__(self, port, peers):
        self.my_id = port
        self.socket = context.socket(zmq.ROUTER)
        self.socket.setsockopt(zmq.IDENTITY, f"{self.my_id}".encode())
        self.reentrant_lock = RLock()

        self.peer_ids = []
        for ip, port in peers:
            self.peer_ids.append(port)
            self.socket.connect(f"tcp://{ip}:{port}")
        # give time to actually connect
        time.sleep(WAIT_TIME_TO_CONNECT_PEERS)

    def broadcast_dict_to_peers(self, message_dict):
        self.broadcast_to_peers(json.dumps(message_dict))

    def broadcast_to_peers(self, message):
        for peer_id in self.peer_ids:
            self.send_to_peer(peer_id, message)
        debug_print(self.my_id, "sent all messages")

    def send_to_peer(self, peer_id, message):
        self.reentrant_lock.acquire()
        debug_print(self.my_id, f'sending "{message}" to', peer_id)
        self.socket.send_multipart([f"{peer_id}".encode(), message.encode()])
        self.reentrant_lock.release()


class ZMQReceiver:
    def __init__(self, ip, port, recv_handler):
        self.my_id = port
        self.socket = context.socket(zmq.ROUTER)
        self.socket.setsockopt(zmq.IDENTITY, f"{self.my_id}".encode())
        self.socket.bind(f"tcp://{ip}:{port}")
        self.recv_handler = recv_handler
        self.thread = Thread(target=self.start_receiving)
        self.thread.start()

    def start_receiving(self):
        while True:
            sender_id, sender_message = self.socket.recv_multipart()
            self.recv_handler(sender_id.decode(), sender_message.decode())
            time.sleep(1e-5)

    def join(self):
        self.thread.join()


def receive_handler(sender_id, sender_message):
    debug_print(
        " server received: ",
        sender_message,
        " from: ",
        sender_id,
    )
