from quantum_sim import ZERO, ONE, X, H, Z, apply_gate, probabilities, pretty_state, measure


print("One-Qubit Demo")
print()


state = ZERO
print("Initial |0> state:")
print("State:", pretty_state(state))
print("Probabilities:", probabilities(state))
print()


state = apply_gate(X, ZERO)
print("After applying X to |0>:")
print("State:", pretty_state(state))
print("Probabilities:", probabilities(state))
print()


state = apply_gate(H, ZERO)
print("After applying H to |0>:")
print("State:", pretty_state(state))
print("Probabilities:", probabilities(state))
print("Measurement:", measure(state, shots=1000))
print()


state = ZERO
state = apply_gate(H, state)
state = apply_gate(Z, state)
state = apply_gate(H, state)

print("After applying H, then Z, then H to |0>:")
print("State:", pretty_state(state))
print("Probabilities:", probabilities(state))
print("Measurement:", measure(state, shots=1000))