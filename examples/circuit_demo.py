from circuit import QuantumCircuit


print("QuantumCircuit Class Demo")
print()


qc = QuantumCircuit(2)

qc.h(0)
qc.cnot(0, 1)

print("Bell state using QuantumCircuit:")
print("State:", qc.pretty())
print("Probabilities:", qc.probabilities())
print("Measurement:", qc.measure(shots=1000))
print()


qc = QuantumCircuit(2)

qc.x(1)
qc.cnot(1, 0)

print("Reverse CNOT using QuantumCircuit:")
print("Start with |01>, then CNOT control=1 target=0")
print("State:", qc.pretty())
print("Probabilities:", qc.probabilities())
print("Measurement:", qc.measure(shots=1000))