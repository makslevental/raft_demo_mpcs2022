import time
from threading import RLock, Thread

import zmq

from logg import debug_print

WAIT_TIME_TO_CONNECT_PEERS = 1
context = zmq.Context()


class ZMQSender:
    def __init__(self, port, peers):
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
            self.send_to_peer(peer_id, message.encode())
        debug_print(self.my_id, "sent all messages")

    def send_to_peer(self, peer_id, message):
        self.reentrant_lock.acquire()
        debug_print(self.my_id.decode(), f'sending "{message}" to', peer_id.decode())
        self.socket.send_multipart([peer_id, message.encode()])
        self.reentrant_lock.release()


class ZMQReceiver:
    def __init__(self, ip, port, recv_handler):
        self.my_id = port.encode()
        self.socket = context.socket(zmq.ROUTER)
        self.socket.setsockopt(zmq.IDENTITY, port.encode())
        self.socket.bind(f"tcp://{ip}:{port}")
        self.recv_handler = recv_handler
        self.thread = Thread(target=self.start_receiving)
        self.thread.start()

    def start_receiving(self):
        while True:
            sender_id, sender_message = self.socket.recv_multipart()
            self.recv_handler(sender_id.decode(), sender_message.decode())
            time.sleep(1e-5)

    def __del__(self):
        self.thread.join(100)
