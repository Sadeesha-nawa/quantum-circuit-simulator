# Quantum Circuit Simulator from Scratch

An educational quantum circuit simulator built from scratch in Python using NumPy.

I started this project to understand the linear algebra behind quantum computing instead of only using high-level libraries like Qiskit. The simulator represents quantum states as vectors, quantum gates as matrices, and applies gates using matrix multiplication.

The project currently supports single-qubit gates, tensor products, multi-qubit states, CNOT gates, Bell-state generation, simulated measurement, and a simple `QuantumCircuit` class interface.

---

## Features

- Represent single-qubit states such as `|0>` and `|1>`
- Apply common quantum gates:
  - Identity gate
  - Pauli-X gate
  - Pauli-Y gate
  - Pauli-Z gate
  - Hadamard gate
  - S gate
  - T gate
- Calculate measurement probabilities from quantum amplitudes
- Simulate measurement over many shots
- Build multi-qubit states using tensor products
- Apply single-qubit gates to selected qubits in a multi-qubit system
- Apply CNOT gates with flexible control and target qubits
- Generate Bell states
- Use a simple `QuantumCircuit` class interface
- Run automatic tests with `pytest`

---

## Project Structure

```text
quantum-circuit-simulator/
│
├── quantum_sim.py
├── circuit.py
├── demo.py
├── examples/
│   ├── one_qubit_demo.py
│   ├── two_qubit_demo.py
│   ├── bell_state_demo.py
│   └── circuit_demo.py
├── tests/
│   └── test_quantum_sim.py
├── pytest.ini
├── requirements.txt
└── README.md
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Sadeesha-nawa/quantum-circuit-simulator.git
cd quantum-circuit-simulator
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment on Windows PowerShell:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Main Demo

```bash
python demo.py
```

Example output:

```text
Quantum Circuit Simulator Demo

Circuit: H on qubit 0, then CNOT control=0 target=1
State: (0.707+0.000j)|00> + (0.707+0.000j)|11>
Probabilities: [0.5 0.  0.  0.5]
Measurement: {'00': 503, '01': 0, '10': 0, '11': 497}
```

This creates a Bell state:

```text
(1/sqrt(2))|00> + (1/sqrt(2))|11>
```

---

## Running Examples

```bash
python -m examples.one_qubit_demo
python -m examples.two_qubit_demo
python -m examples.bell_state_demo
python -m examples.circuit_demo
```

---

## Running Tests

This project uses `pytest`.

```bash
pytest
```

Expected result:

```text
10 passed
```

The tests verify behavior such as:

- `X|0> = |1>`
- Applying `H` twice returns the original state
- `CNOT|10> = |11>`
- Reverse CNOT works
- Bell-state probabilities are correct
- `QuantumCircuit` creates the expected Bell state

---

## Main Concepts Implemented

### States as Vectors

The simulator represents quantum states as NumPy vectors.

```text
|0> = [1, 0]
|1> = [0, 1]
```

A general one-qubit state is:

```text
|ψ> = a|0> + b|1>
```

where `a` and `b` are complex amplitudes.

The probability of measuring each state is found using:

```text
P(state) = |amplitude|²
```

---

### Gates as Matrices

Quantum gates are represented as matrices and applied using matrix multiplication.

```python
new_state = gate @ state
```

---

### Tensor Products

Multi-qubit states are created using tensor products.

```text
|0> ⊗ |1> = |01>
```

For two qubits, this simulator uses the basis order:

```text
|00>, |01>, |10>, |11>
```

So the basis states are represented as:

```text
|00> = [1, 0, 0, 0]
|01> = [0, 1, 0, 0]
|10> = [0, 0, 1, 0]
|11> = [0, 0, 0, 1]
```

---

### CNOT

The CNOT gate uses a control qubit and a target qubit.

- If the control qubit is `1`, flip the target qubit.
- If the control qubit is `0`, do nothing.

The simulator supports flexible CNOT gates:

```python
cnot_gate(num_qubits, control, target)
```

---

## What I Learned

Through this project, I practiced:

- Representing quantum states with vectors
- Using complex amplitudes and probabilities
- Applying gates through matrix multiplication
- Building multi-qubit states with tensor products
- Implementing CNOT gates from basis-state mappings
- Simulating measurement using probability distributions
- Organizing a Python project with examples and tests

---

## Future Improvements

Possible future additions:

- Add more controlled gates
- Add circuit history/logging
- Add simple circuit diagrams
- Add Grover’s algorithm or Deutsch-Jozsa algorithm demo
- Compare simulator output with Qiskit