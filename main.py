import json
import sys
import time

from routes import app
from timer import ResettableTimer
from logg import debug_print


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

    assert my_ip, my_port
    return my_ip, my_port, peers


start_time = time.time()


def log_time_taken():
    global start_time
    debug_print("Time's Up! Took ", time.time() - start_time, "seconds")
    start_time = time.time()
    timer.reset()


if __name__ == "__main__":
    config_json_fp = sys.argv[1]
    config_json_idx = int(sys.argv[2])
    _my_ip, my_port, peers = parse_config_json(config_json_fp, config_json_idx)

    timer = ResettableTimer(log_time_taken, interval_lb=1000, interval_ub=2000)
    timer.run()

    app.run(debug=True, host="localhost", port=my_port, threaded=True)
