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

# Core simulator functions

def apply_gate(gate, state):
    """
    Apply a quantum gate to a quantum state.
    """
    return gate @ state


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
    Return a readable string version of a one-qubit quantum state.
    """
    labels = ["|0>", "|1>"]
    terms = []

    for amplitude, label in zip(state, labels):
        if abs(amplitude) > 1e-10:
            terms.append(f"({amplitude:.3f}){label}")

    return " + ".join(terms) if terms else "0"


def measure(state, shots=1000):
    """
    Simulate measuring a one-qubit quantum state multiple times.

    Returns a dictionary with counts for outcomes '0' and '1'.
    """
    probs = probabilities(state)

    outcomes = np.random.choice([0, 1], size=shots, p=probs)

    return {
        "0": int(np.sum(outcomes == 0)),
        "1": int(np.sum(outcomes == 1))
    }

