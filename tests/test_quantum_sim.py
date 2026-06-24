import numpy as np

from quantum_sim import (
    ZERO,
    ONE,
    I,
    X,
    H,
    CNOT,
    tensor_product,
    apply_gate,
    apply_single_qubit_gate,
    probabilities,
    cnot_gate,
)
from circuit import QuantumCircuit


def test_x_gate_flips_zero_to_one():
    state = apply_gate(X, ZERO)

    assert np.allclose(state, ONE)


def test_h_gate_creates_equal_superposition():
    state = apply_gate(H, ZERO)

    expected = (1 / np.sqrt(2)) * np.array([1, 1], dtype=complex)

    assert np.allclose(state, expected)


def test_h_gate_applied_twice_returns_original_state():
    state = ZERO

    state = apply_gate(H, state)
    state = apply_gate(H, state)

    assert np.allclose(state, ZERO)


def test_probabilities_sum_to_one():
    state = apply_gate(H, ZERO)

    probs = probabilities(state)

    assert np.isclose(np.sum(probs), 1.0)


def test_tensor_product_zero_one_creates_01_state():
    state = tensor_product(ZERO, ONE)

    expected = np.array([0, 1, 0, 0], dtype=complex)

    assert np.allclose(state, expected)


def test_standard_cnot_maps_10_to_11():
    state = tensor_product(ONE, ZERO)

    new_state = apply_gate(CNOT, state)

    expected = tensor_product(ONE, ONE)

    assert np.allclose(new_state, expected)


def test_flexible_cnot_control_1_target_0_maps_01_to_11():
    state = tensor_product(ZERO, ONE)

    gate = cnot_gate(2, control=1, target=0)
    new_state = apply_gate(gate, state)

    expected = tensor_product(ONE, ONE)

    assert np.allclose(new_state, expected)


def test_apply_single_qubit_gate_to_first_qubit():
    state = tensor_product(ZERO, ZERO)

    new_state = apply_single_qubit_gate(state, H, target=0)

    expected = (1 / np.sqrt(2)) * (
        tensor_product(ZERO, ZERO) + tensor_product(ONE, ZERO)
    )

    assert np.allclose(new_state, expected)


def test_bell_state_probabilities():
    state = tensor_product(ZERO, ZERO)

    state = apply_gate(tensor_product(H, I), state)
    state = apply_gate(CNOT, state)

    expected_probs = np.array([0.5, 0.0, 0.0, 0.5])

    assert np.allclose(probabilities(state), expected_probs)


def test_quantum_circuit_bell_state():
    qc = QuantumCircuit(2)

    qc.h(0)
    qc.cnot(0, 1)

    expected_probs = np.array([0.5, 0.0, 0.0, 0.5])

    assert np.allclose(qc.probabilities(), expected_probs)

def test_quantum_circuit_history_records_gates():
    qc = QuantumCircuit(2)

    qc.h(0)
    qc.cnot(0, 1)

    assert qc.history == [
        "H on qubit 0",
        "CNOT control=0 target=1",
    ]


def test_quantum_circuit_summary():
    qc = QuantumCircuit(2)

    qc.h(0)
    qc.cnot(0, 1)

    expected = "1. H on qubit 0\n2. CNOT control=0 target=1"

    assert qc.summary() == expected


def test_quantum_circuit_reset_clears_history():
    qc = QuantumCircuit(2)

    qc.h(0)
    qc.cnot(0, 1)
    qc.reset()

    assert qc.history == []
    assert qc.summary() == "No gates applied."