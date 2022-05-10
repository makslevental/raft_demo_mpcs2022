import json
import sys
import time

import zmq

config_json = json.load(open("config.json"))
id = int(sys.argv[1])

my_ip, my_port = None, None
peers = []
for i, address in enumerate(config_json["addresses"]):
    ip, port = address["ip"], str(address["port"])
    if i == id:
        my_ip, my_port = ip, port
    else:
        peers.append((ip, port))

context = zmq.Context()

receiving_socket = context.socket(zmq.ROUTER)
receiving_socket.setsockopt(zmq.IDENTITY, my_port.encode())
receiving_socket.bind(f"tcp://{my_ip}:{my_port}")

sending_socket = context.socket(zmq.ROUTER)
sending_socket.setsockopt(zmq.IDENTITY, my_port.encode())

for ip, port in peers:
    sending_socket.connect(f"tcp://{ip}:{port}")

time.sleep(1)

for ip, port in peers:
    message_for_recipient = b"coucou!"
    print(my_port, " sending a message to ", port)
    sending_socket.send_multipart([port.encode(), message_for_recipient])

while True:
    # Receive a message from peer
    sender_id, sender_message = receiving_socket.recv_multipart()

    print(
        my_port,
        " server received: ",
        sender_message.decode(),
        " from: ",
        sender_id.decode(),
    )

    if sender_message.decode() != "got your message":
        sending_socket.send_multipart([sender_id, "got your message".encode()])
