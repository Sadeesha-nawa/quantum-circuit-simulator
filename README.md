# Quantum Circuit Simulator from Scratch

An educational quantum circuit simulator built from scratch in Python using NumPy, with an interactive browser version powered by Pyodide.

I started this project to understand the linear algebra behind quantum computing instead of only using high-level libraries like Qiskit. The simulator represents quantum states as vectors, quantum gates as matrices, and applies gates using matrix multiplication.

The project currently supports single-qubit gates, tensor products, multi-qubit states, flexible CNOT gates, Bell-state generation, simulated measurement, a simple `QuantumCircuit` class interface, automated tests, and a browser-based circuit builder.

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
- Track circuit history and print a readable circuit summary
- Run automatic tests with `pytest`
- Use an interactive browser-based circuit builder with Pyodide

---

## Browser Web App

This project includes an interactive browser-based version of the simulator built with HTML, CSS, JavaScript, and Pyodide.

The web app lets users build small quantum circuits directly in the browser. It loads the Python/NumPy simulator through Pyodide, sends circuit operations from JavaScript to Python, runs the simulation, and displays the final state, measurement probabilities, and simulated measurement results.

### Web App Features

- Runs the Python simulator directly in the browser with Pyodide
- Interactive circuit builder for 1-3 qubits
- Supports gates: H, X, Y, Z, S, T, and CNOT
- Bell state example button
- Custom measurement shot count
- Formatted basis-state probabilities
- Simulated measurement results
- CNOT validation for control and target qubits
- No local Python installation required for users once deployed online

---

## Project Structure

```text
quantum-circuit-simulator/
├── quantum_sim.py              # Core simulator functions, states, gates, measurement
├── circuit.py                  # QuantumCircuit class interface
├── demo.py                     # Main demo script
├── requirements.txt            # Python dependencies
├── pytest.ini                  # Pytest configuration
├── README.md                   # Project documentation
├── examples/                   # Example scripts
│   ├── one_qubit_demo.py
│   ├── two_qubit_demo.py
│   ├── bell_state_demo.py
│   └── circuit_demo.py
├── tests/                      # Automated tests
│   └── test_quantum_sim.py
└── web/                        # Browser-based simulator
    ├── index.html              # Web app structure
    ├── styles.css              # Web app styling
    ├── app.js                  # JavaScript/Pyodide logic
    └── python/
        ├── quantum_sim.py      # Simulator copy used by Pyodide
        ├── circuit.py          # QuantumCircuit class used by Pyodide
        └── web_runner.py       # Browser-facing Python runner functions
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

Circuit:
1. H on qubit 0
2. CNOT control=0 target=1

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

## Running the Web App Locally

From the project root:

```bash
cd web
python -m http.server 8000
```

Then open:

```text
http://localhost:8000/
```

The web app should load Pyodide, NumPy, and the simulator files in the browser.

Do not open `index.html` directly by double-clicking it. The app loads Python files using browser `fetch()` requests, so it should be served through a local server.

### Example Web Circuit

A Bell state can be created in the web app by clicking the Bell state example button or manually adding:

```text
1. H on qubit 0
2. CNOT control=0 target=1
```

Expected probabilities:

```text
|00>: 0.5
|01>: 0
|10>: 0
|11>: 0.5
```

A 3-qubit GHZ state can be created by adding:

```text
1. H on qubit 0
2. CNOT control=0 target=1
3. CNOT control=0 target=2
```

Expected probabilities:

```text
|000>: 0.5
|001>: 0
|010>: 0
|011>: 0
|100>: 0
|101>: 0
|110>: 0
|111>: 0.5
```

---

## Running Tests

This project uses `pytest`.

```bash
pytest
```

Expected result:

```text
13 passed
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

## How the Browser Version Works

The browser app uses Pyodide to run Python inside the browser through WebAssembly.

The browser workflow is:

```text
HTML/CSS creates the page
JavaScript loads Pyodide and NumPy
JavaScript loads the Python simulator files
The user builds a circuit in the UI
JavaScript sends the circuit operations to Python as JSON
Python runs the simulation
Python returns the result as JSON
JavaScript displays the formatted output
```

This allows users to try the simulator from a web page without installing Python locally once the app is deployed.

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
- Building a simple browser interface around Python code
- Using Pyodide to run Python/NumPy code in the browser
- Passing data between JavaScript and Python with JSON

---

## Future Improvements

Possible future improvements include:

- Deploy the browser version with GitHub Pages
- Add more quantum gates and controlled gates
- Add visual circuit diagrams
- Support more qubits with performance warnings
- Add additional algorithm demos such as Deutsch-Jozsa or Grover search
- Add automated tests for the web runner
- Improve synchronization between the root Python simulator files and the web Python files
- Compare simulator output with Qiskit
