from quantum_sim import ZERO, ONE, I, X, Y, Z, H, S, T, CNOT, apply_gate, probabilities, pretty_state, measure, is_unitary, tensor_product

print("Testing the one-qubit simulator")
print()


# Test 1: Start in |0>
state = ZERO

print("Initial state |0>:")
print("Raw vector:", state)
print("Pretty state:", pretty_state(state))
print("Probabilities:", probabilities(state))
print("Measurement:", measure(state, shots=1000))
print()


# Test 2: Apply X to |0>
state = apply_gate(X, ZERO)

print("After applying X to |0>:")
print("Raw vector:", state)
print("Pretty state:", pretty_state(state))
print("Probabilities:", probabilities(state))
print("Measurement:", measure(state, shots=1000))
print()


# Test 3: Apply X to |1>
state = apply_gate(X, ONE)

print("After applying X to |1>:")
print("Raw vector:", state)
print("Pretty state:", pretty_state(state))
print("Probabilities:", probabilities(state))
print("Measurement:", measure(state, shots=1000))
print()


# Test 4: Apply H to |0>
state = apply_gate(H, ZERO)

print("After applying H to |0>:")
print("Raw vector:", state)
print("Pretty state:", pretty_state(state))
print("Probabilities:", probabilities(state))
print("Measurement:", measure(state, shots=1000))
print()


# Test 5: Apply H twice to |0>
state = apply_gate(H, ZERO)
state = apply_gate(H, state)

print("After applying H twice to |0>:")
print("Raw vector:", state)
print("Pretty state:", pretty_state(state))
print("Probabilities:", probabilities(state))
print("Measurement:", measure(state, shots=1000))
print()

# Test 6: Demonstrate phase/interference with H, Z, H
state = ZERO
state = apply_gate(H, state)
state = apply_gate(Z, state)
state = apply_gate(H, state)

print("After applying H, then Z, then H to |0>:")
print("Raw vector:", state)
print("Pretty state:", pretty_state(state))
print("Probabilities:", probabilities(state))
print("Measurement:", measure(state, shots=1000))
print()

# Test 7: Check which gates are unitary
print("Checking if basic gates are unitary:")

gates = {
    "I": I,
    "X": X,
    "Y": Y,
    "Z": Z,
    "H": H,
    "S": S,
    "T": T
}

for name, gate in gates.items():
    print(f"{name} is unitary:", is_unitary(gate))

print()

# Test 8: Create two-qubit basis states using tensor products
zero_zero = tensor_product(ZERO, ZERO)
zero_one = tensor_product(ZERO, ONE)
one_zero = tensor_product(ONE, ZERO)
one_one = tensor_product(ONE, ONE)

print("Two-qubit basis states:")
print("|00> =", zero_zero)
print("|01> =", zero_one)
print("|10> =", one_zero)
print("|11> =", one_one)
print()


# Test 9: Apply H to both qubits in |00>
state = zero_zero

H_both = tensor_product(H, H)
state = apply_gate(H_both, state)

print("After applying H ⊗ H to |00>:")
print("Raw vector:", state)
print("Pretty state:", pretty_state(state))
print("Probabilities:", probabilities(state))
print("Measurement:", measure(state, shots=1000))
print()


# Test 10: CNOT on two-qubit basis states
print("Testing CNOT gate:")

basis_states = {
    "|00>": tensor_product(ZERO, ZERO),
    "|01>": tensor_product(ZERO, ONE),
    "|10>": tensor_product(ONE, ZERO),
    "|11>": tensor_product(ONE, ONE),
}

for label, state in basis_states.items():
    new_state = apply_gate(CNOT, state)
    print(f"CNOT{label} =", pretty_state(new_state))
print()


# Test 11: Create a Bell state
state = tensor_product(ZERO, ZERO)

state = apply_gate(tensor_product(H, I), state)
state = apply_gate(CNOT, state)

print("Bell state from applying H ⊗ I, then CNOT to |00>:")
print("Raw vector:", state)
print("Pretty state:", pretty_state(state))
print("Probabilities:", probabilities(state))
print("Measurement:", measure(state, shots=1000))
print()