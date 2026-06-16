import numpy as np

# Basic one-qubit states

ZERO = np.array([1, 0], dtype=complex)  # |0>
ONE = np.array([0, 1], dtype=complex)   # |1>

# Basic one-qubit gates

# -----------------------------
# Basic one-qubit gates
# -----------------------------

I = np.array([
    [1, 0],
    [0, 1]
], dtype=complex)

X = np.array([
    [0, 1],
    [1, 0]
], dtype=complex)

Y = np.array([
    [0, -1j],
    [1j, 0]
], dtype=complex)

Z = np.array([
    [1, 0],
    [0, -1]
], dtype=complex)

H = (1 / np.sqrt(2)) * np.array([
    [1, 1],
    [1, -1]
], dtype=complex)

S = np.array([
    [1, 0],
    [0, 1j]
], dtype=complex)

T = np.array([
    [1, 0],
    [0, np.exp(1j * np.pi / 4)]
], dtype=complex)

CNOT = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 1, 0]
], dtype=complex)

# Core simulator functions

def apply_gate(gate, state):
    """
    Apply a quantum gate to a quantum state.
    """
    return gate @ state

def apply_single_qubit_gate(state, gate, target):
    """
    Apply a one-qubit gate to a specific qubit in a multi-qubit state.

    target = 0 means the first/leftmost qubit.
    target = 1 means the second qubit.
    """
    n = num_qubits(state)

    if target < 0 or target >= n:
        raise ValueError("Target qubit index is out of range.")

    operators = []

    for qubit in range(n):
        if qubit == target:
            operators.append(gate)
        else:
            operators.append(I)

    full_gate = tensor_product(*operators)

    return apply_gate(full_gate, state)

def tensor_product(*items):
    """
    Compute the tensor product of multiple vectors or matrices.

    Examples:
    tensor_product(ZERO, ZERO) gives |00>
    tensor_product(H, H) gives H ⊗ H
    """
    result = items[0]

    for item in items[1:]:
        result = np.kron(result, item)

    return result

def num_qubits(state):
    """
    Infer the number of qubits from the length of the state vector.

    A 1-qubit state has length 2.
    A 2-qubit state has length 4.
    A 3-qubit state has length 8.
    """
    n = int(np.log2(len(state)))

    if 2 ** n != len(state):
        raise ValueError("State vector length must be a power of 2.")

    return n


def basis_labels(n):
    """
    Generate computational basis labels for n qubits.

    For n = 1: ['0', '1']
    For n = 2: ['00', '01', '10', '11']
    For n = 3: ['000', '001', ..., '111']
    """
    return [format(i, f"0{n}b") for i in range(2 ** n)]

def probabilities(state):
    """
    Convert quantum amplitudes into measurement probabilities.
    """
    return np.abs(state) ** 2

def is_unitary(gate):
    """
    Check whether a gate is unitary.

    A gate U is unitary if U†U = I.
    """
    identity = np.eye(gate.shape[0], dtype=complex)
    return np.allclose(gate.conj().T @ gate, identity)

def pretty_state(state):
    """
    Return a readable string version of a quantum state.
    Works for one-qubit and multi-qubit states.
    """
    n = num_qubits(state)
    labels = basis_labels(n)
    terms = []

    for amplitude, label in zip(state, labels):
        if abs(amplitude) > 1e-10:
            terms.append(f"({amplitude:.3f})|{label}>")

    return " + ".join(terms) if terms else "0"


def measure(state, shots=1000):
    """
    Simulate measuring a quantum state multiple times.

    Returns a dictionary with counts for each possible outcome.
    """
    probs = probabilities(state)
    probs = probs / np.sum(probs)
    n = num_qubits(state)
    labels = basis_labels(n)

    outcomes = np.random.choice(labels, size=shots, p=probs)

    return {
        label: int(np.sum(outcomes == label))
        for label in labels
    }

