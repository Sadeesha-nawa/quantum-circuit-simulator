from quantum_sim import ZERO, I, H, CNOT, tensor_product, apply_gate, probabilities, pretty_state, measure


print("Bell State Demo")
print()


state = tensor_product(ZERO, ZERO)

state = apply_gate(tensor_product(H, I), state)
state = apply_gate(CNOT, state)

print("Bell state from applying H ⊗ I, then CNOT to |00>:")
print("State:", pretty_state(state))
print("Probabilities:", probabilities(state))
print("Measurement:", measure(state, shots=1000))