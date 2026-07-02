import json

from circuit import QuantumCircuit


def circuit_result(qc, shots=1000):
    """
    Convert a QuantumCircuit object into browser-friendly JSON.
    """
    result = {
        "summary": qc.summary(),
        "state": qc.pretty(),
        "probabilities": [round(float(p), 6) for p in qc.probabilities()],
        "measurement": qc.measure(shots=shots),
    }

    return json.dumps(result)


def run_bell_demo(shots=1000):
    """
    Run a Bell-state circuit and return browser-friendly JSON.
    """
    qc = QuantumCircuit(2)

    qc.h(0)
    qc.cnot(0, 1)

    return circuit_result(qc, shots=shots)


def run_circuit(num_qubits, operations_json, shots=1000):
    """
    Run a custom circuit from a JSON list of operations.
    """
    operations = json.loads(operations_json)

    qc = QuantumCircuit(num_qubits)

    for operation in operations:
        gate = operation["gate"]

        if gate == "H":
            qc.h(operation["target"])
        elif gate == "X":
            qc.x(operation["target"])
        elif gate == "Y":
            qc.y(operation["target"])
        elif gate == "Z":
            qc.z(operation["target"])
        elif gate == "S":
            qc.s(operation["target"])
        elif gate == "T":
            qc.t(operation["target"])
        elif gate == "CNOT":
            qc.cnot(operation["control"], operation["target"])
        else:
            raise ValueError(f"Unknown gate: {gate}")

    return circuit_result(qc, shots=shots)