import json

from circuit import QuantumCircuit


def run_bell_demo(shots=1000):
    """
    Run a Bell-state circuit and return browser-friendly JSON.
    """
    qc = QuantumCircuit(2)

    qc.h(0)
    qc.cnot(0, 1)

    result = {
        "summary": qc.summary(),
        "state": qc.pretty(),
        "probabilities": [float(p) for p in qc.probabilities()],
        "measurement": qc.measure(shots=shots),
    }

    return json.dumps(result)