from flask import Flask, request, jsonify, send_from_directory, Response, stream_with_context
from LIF import LIF
from Network import Network
from flask_cors import CORS
import random
import json
import time

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route('/stream', methods=['GET'])
def stream():
    excitatory = float(request.args.get('excitatory', 3.0))
    inhibitory = float(request.args.get('inhibitory', 1.0))
    weight = float(request.args.get('weight', 5.0))
    p = float(request.args.get('p', 0.5))
    duration = int(request.args.get('duration', 200))

    sources = [LIF(vm_init=random.uniform(-70, -60),
                   leak=random.uniform(0.04, 0.06),
                   threshold=random.uniform(-57, -53)) for _ in range(5)]

    targets = [LIF(vm_init=random.uniform(-70, -60),
                   leak=random.uniform(0.01, 0.02),
                   threshold=random.uniform(-57, -53)) for _ in range(5)]

    network = Network(sources, targets, p=p, weight=weight)
    network.connect()

    def generate():
        # Send connectivity once at t=0
        synapses = [{"source": sources.index(s.source),
                     "target": targets.index(s.target),
                     "weight": s.weight}
                    for s in network.synapses]

        for t in range(duration):
            for src in sources:
                exc = excitatory + random.gauss(0, 0.5)
                inh = inhibitory + random.gauss(0, 0.2)
                src.step(t, excitatory=exc, inhibitory=inh)
            for trg in targets:
                trg.step(t)
            for snp in network.synapses:
                snp.step(t)

            state = {
                "t": t,
                "sources": [{"voltage": src.voltages[-1], "fired": t in src.spike_times} for src in sources],
                "targets": [{"voltage": trg.voltages[-1], "fired": t in trg.spike_times} for trg in targets],
                "synapses": synapses if t == 0 else None
            }

            yield f"data: {json.dumps(state)}\n\n"
            time.sleep(0.03)

    return Response(stream_with_context(generate()), mimetype='text/event-stream')


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
        ],
        "synapses": [
            {"source": sources.index(snp.source), "target": targets.index(snp.target), "weight": snp.weight}
            for snp in network.synapses
        ]
    })


if __name__ == '__main__':
    app.run(debug=True)
