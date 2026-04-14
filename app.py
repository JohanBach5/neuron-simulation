from flask import Flask, request, jsonify, send_from_directory
from LIF import LIF
from Network import Network
from flask_cors import CORS
import random


app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    data = request.get_json()
    sources = [LIF(vm_init=random.uniform(-70, -60),
                   leak=random.uniform(0.04, 0.06),
                   threshold=random.uniform(-57, -53)) for _ in range(5)]

    targets = [LIF(vm_init=random.uniform(-70, -60),
                   leak=random.uniform(0.04, 0.06),
                   threshold=random.uniform(-57, -53)) for _ in range(5)]

    network = Network(sources, targets, p=0.5)
    network.connect()

    for t in range(200):
        for src in sources:
            excitatory = 3.0 + random.gauss(0, 0.5)
            inhibitory = 1.0 + random.gauss(0, 0.2)
            src.step(t, excitatory=excitatory, inhibitory=inhibitory)
        for trg in targets:
            trg.step(t)
        for snp in network.synapses:
            snp.step(t)

    return jsonify({
        "sources": [
            {"times": src.times, "voltages": src.voltages, "spike_times": src.spike_times}
            for src in sources
        ],
        "targets": [
            {"times": trg.times, "voltages": trg.voltages, "spike_times": trg.spike_times}
            for trg in targets
        ]
    })


if __name__ == '__main__':
    app.run(debug=True)
