import time
from threading import Thread
from typing import List

import zmq

SEND_RULE = {
    '5555': '6666',
    '6666': '7777',
    '7777': '5555'
}


def worker(socket_port: str, peer_ports: List[str]):
    context = zmq.Context()

    receiving_socket = context.socket(zmq.ROUTER)
    receiving_socket.setsockopt(zmq.IDENTITY, socket_port.encode())
    receiving_socket.bind(f'tcp://*:{socket_port}')

    sending_socket = context.socket(zmq.ROUTER)
    sending_socket.setsockopt(zmq.IDENTITY, socket_port.encode())

    for peer_port in peer_ports:
        sending_socket.connect(f'tcp://localhost:{peer_port}')

    time.sleep(1)

    recipient_id = SEND_RULE[socket_port].encode()
    message_for_recipient = b'coucou!'

    print(socket_port, ' sending a message to ', recipient_id.decode())
    sending_socket.send_multipart([recipient_id, message_for_recipient])

    # Receive a message from peer
    sender_id, sender_message = receiving_socket.recv_multipart()

    print(socket_port,
          ' server received: ',
          sender_message.decode(),
          ' from: ',
          sender_id.decode()
          )


if __name__ == '__main__':
    socket_ports = ['5555', '6666', '7777']
    for socket_port in socket_ports:
        Thread(target=worker,
               args=(socket_port,
                     [port for port in socket_ports
                      if port != socket_ports]
                     )
               ).start()

    time.sleep(3)
