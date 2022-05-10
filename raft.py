import dataclasses
import json
from dataclasses import dataclass
from enum import Enum

from logg import debug_print
from timer import ResettableTimer


class Role(Enum):
    Follower = "Follower"
    Leader = "Leader"
    Candidate = "Candidate"


@dataclass
class PersistentState:
    pass


@dataclass
class LogEntry:
    message: str
    term: int


@dataclass
class VoteRequest:
    term: int
    candidate_id: int
    last_log_index: int
    last_log_term: int


def serialize(rpc):
    return {"class": rpc.__class__.__qualname__, "dict": dataclasses.asdict(rpc)}


def deserialize(rpc_dict_str):
    rpc_dict = json.loads(rpc_dict_str)
    return globals()[rpc_dict["class"]](**rpc_dict["dict"])


class Node:
    def __init__(self, id, broadcast_fn):
        self.id = id
        self.broadcast_fn = broadcast_fn
        self.current_term = 0
        self.role = Role.Candidate
        self.log = []
        self.election_timer = ResettableTimer(self.run_election)
        self.election_timer.start()

    def rpc_handler(self, sender_id, rpc_message_dict_str):
        debug_print("received rpc str", sender_id, rpc_message_dict_str)
        rpc_message = deserialize(rpc_message_dict_str)
        debug_print("received rpc", rpc_message)

    def run_election(self):
        self.election_timer.start()
        if self.role == Role.Leader:
            return

        debug_print("starting election")
        self.broadcast_fn(
            serialize(
                VoteRequest(
                    self.current_term,
                    self.id,
                    self.get_last_log_index(),
                    self.get_last_log_term(),
                )
            )
        )

    def get_last_log_index(self):
        return len(self.log) - 1

    def get_last_log_term(self):
        return self.log[self.get_last_log_index()].term if len(self.log) else -1
