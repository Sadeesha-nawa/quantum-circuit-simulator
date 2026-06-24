from quantum_sim import (
    ZERO,
    X,
    Y,
    Z,
    H,
    S,
    T,
    tensor_product,
    apply_gate,
    apply_single_qubit_gate,
    probabilities,
    pretty_state,
    measure,
    cnot_gate,
)


class QuantumCircuit:
    """
    A simple quantum circuit simulator.

    Stores a quantum state and allows gates to be applied step by step.
    Also keeps a history of gates that have been applied.
    """

    def __init__(self, num_qubits):
        """
        Create a quantum circuit with num_qubits qubits.

        The circuit starts in the all-zero state.
        For 1 qubit: |0>
        For 2 qubits: |00>
        For 3 qubits: |000>
        """
        if num_qubits < 1:
            raise ValueError("A circuit must have at least one qubit.")

        self.num_qubits = num_qubits
        self.state = tensor_product(*([ZERO] * num_qubits))
        self.history = []

    def apply(self, gate, target, gate_name="CUSTOM"):
        """
        Apply a one-qubit gate to a chosen target qubit.

        The gate is also recorded in the circuit history.
        """
        self.state = apply_single_qubit_gate(self.state, gate, target)
        self.history.append(f"{gate_name} on qubit {target}")
        return self

    def x(self, target):
        return self.apply(X, target, "X")

    def y(self, target):
        return self.apply(Y, target, "Y")

    def z(self, target):
        return self.apply(Z, target, "Z")

    def h(self, target):
        return self.apply(H, target, "H")

    def s(self, target):
        return self.apply(S, target, "S")

    def t(self, target):
        return self.apply(T, target, "T")

    def cnot(self, control, target):
        """
        Apply CNOT with the chosen control and target qubits.

        If the control qubit is 1, the target qubit is flipped.
        The operation is also recorded in the circuit history.
        """
        gate = cnot_gate(self.num_qubits, control, target)
        self.state = apply_gate(gate, self.state)
        self.history.append(f"CNOT control={control} target={target}")
        return self

    def probabilities(self):
        """
        Return measurement probabilities for the current state.
        """
        return probabilities(self.state)

    def measure(self, shots=1000):
        """
        Simulate measuring the current state.
        """
        return measure(self.state, shots=shots)

    def pretty(self):
        """
        Return a readable ket-notation version of the current state.
        """
        return pretty_state(self.state)

    def summary(self):
        """
        Return a readable numbered list of gates applied to the circuit.
        """
        if not self.history:
            return "No gates applied."

        lines = []
        for index, operation in enumerate(self.history, start=1):
            lines.append(f"{index}. {operation}")

        return "\n".join(lines)

    def reset(self):
        """
        Reset the circuit back to the all-zero state.

        The circuit history is also cleared.
        """
        self.state = tensor_product(*([ZERO] * self.num_qubits))
        self.history.clear()
        return self