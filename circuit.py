from quantum_sim import (
    ZERO,
    X,
    Y,
    Z,
    H,
    S,
    T,
    CNOT,
    tensor_product,
    apply_gate,
    apply_single_qubit_gate,
    probabilities,
    pretty_state,
    measure,
)


class QuantumCircuit:
    """
    A simple quantum circuit simulator.

    Stores a quantum state and allows gates to be applied step by step.
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

    def apply(self, gate, target):
        """
        Apply a one-qubit gate to a chosen target qubit.
        """
        self.state = apply_single_qubit_gate(self.state, gate, target)
        return self

    def x(self, target):
        return self.apply(X, target)

    def y(self, target):
        return self.apply(Y, target)

    def z(self, target):
        return self.apply(Z, target)

    def h(self, target):
        return self.apply(H, target)

    def s(self, target):
        return self.apply(S, target)

    def t(self, target):
        return self.apply(T, target)

    def cnot(self, control=0, target=1):
        """
        Apply CNOT to a 2-qubit circuit.

        Current version supports:
        control = 0, target = 1
        """
        if self.num_qubits != 2:
            raise NotImplementedError("CNOT currently only supports 2-qubit circuits.")

        if control != 0 or target != 1:
            raise NotImplementedError("Current CNOT supports control=0 and target=1 only.")

        self.state = apply_gate(CNOT, self.state)
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

    def reset(self):
        """
        Reset the circuit back to the all-zero state.
        """
        self.state = tensor_product(*([ZERO] * self.num_qubits))
        return self