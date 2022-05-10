class Node:
    def __init__(self, id, peer_ids):
        self.id = id
        self.peer_ids = peer_ids

    def rpc_handler(self, sender_id, rpc_message):
        print(sender_id, rpc_message)
