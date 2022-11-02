import json
import sys

from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


if __name__ == "__main__":
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

    assert my_port
    app.run(debug=True, host="localhost", port=my_port, threaded=True)
