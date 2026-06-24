from circuit import QuantumCircuit


qc = QuantumCircuit(2)

qc.h(0)
qc.cnot(0, 1)

print("Quantum Circuit Simulator Demo")
print()
print("Circuit:")
print(qc.summary())
print()
print("State:", qc.pretty())
print("Probabilities:", qc.probabilities())
print("Measurement:", qc.measure(shots=1000))