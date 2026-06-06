from quantum_sim import ZERO, ONE, X, Z, H, apply_gate, probabilities, pretty_state, measure

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