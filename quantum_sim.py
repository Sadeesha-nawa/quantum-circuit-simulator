import numpy as np


# -----------------------------
# Basic one-qubit states
# -----------------------------

ZERO = np.array([1, 0], dtype=complex)  # |0>
ONE = np.array([0, 1], dtype=complex)   # |1>


# -----------------------------
# Basic one-qubit gates
# -----------------------------

X = np.array([
    [0, 1],
    [1, 0]
], dtype=complex)

H = (1 / np.sqrt(2)) * np.array([
    [1, 1],
    [1, -1]
], dtype=complex)


# -----------------------------
# Core simulator functions
# -----------------------------

def apply_gate(gate, state):
    """
    Apply a quantum gate to a quantum state.

    gate: matrix representing the quantum gate
    state: vector representing the quantum state
    """
    return gate @ state


def probabilities(state):
    """
    Convert quantum amplitudes into measurement probabilities.

    For a state [a, b], this returns [|a|^2, |b|^2].
    """
    return np.abs(state) ** 2

