from quantum_sim import ZERO, ONE, H, tensor_product, apply_gate, probabilities, pretty_state, measure


print("Two-Qubit Demo")
print()


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


state = zero_zero
H_both = tensor_product(H, H)
state = apply_gate(H_both, state)

print("After applying H ⊗ H to |00>:")
print("State:", pretty_state(state))
print("Probabilities:", probabilities(state))
print("Measurement:", measure(state, shots=1000))