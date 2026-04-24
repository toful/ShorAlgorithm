import numpy as np
from math import gcd, ceil, log2
from fractions import Fraction
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.circuit.library import UnitaryGate


def required_bits(N):
    """
    Computes the number of qubits required
    to represent integers modulo N.
    """
    return ceil(log2(N))


def modular_multiplication_unitary(a, N, n_qubits):
    dim = 2 ** n_qubits
    U = np.zeros((dim, dim))

    for y in range(dim):
        if y < N:
            U[(a * y) % N, y] = 1
        else:
            U[y, y] = 1

    return UnitaryGate(U, label=f"×{a} mod {N}")


def inverse_qft(qc, n):
    for i in range(n // 2):
        qc.swap(i, n - i - 1)
    for j in range(n):
        for m in range(j):
            qc.cp(-np.pi / (2 ** (j - m)), m, j)
        qc.h(j)


def build_shor_circuit(N, a):
    n_target = required_bits(N)
    n_count = n_target  # Standard choice in Shor

    qc = QuantumCircuit(n_count + n_target, n_count)
    qc.h(range(n_count))
    qc.x(n_count)

    for q in range(n_count):
        a_power = pow(a, 2**q, N)
        U = modular_multiplication_unitary(a_power, N, n_target)
        qc.append(
            U.control(),
            [q] + list(range(n_count, n_count + n_target))
        )

    inverse_qft(qc, n_count)
    qc.measure(range(n_count), range(n_count))
    return qc, n_count


def run_shor(N, a, shots=1024):
    qc, n_count = build_shor_circuit(N, a)
    backend = Aer.get_backend("qasm_simulator")
    result = backend.run(transpile(qc, backend), shots=shots).result()
    counts = result.get_counts()
    return counts, n_count, qc


def classical_postprocess(counts, a, N, n_count):
    factors = set()

    for output in counts:
        decimal = int(output, 2)
        phase = decimal / (2 ** n_count)
        frac = Fraction(phase).limit_denominator(N)
        r = frac.denominator

        if r % 2 != 0:
            continue

        f1 = gcd(pow(a, r // 2) - 1, N)
        f2 = gcd(pow(a, r // 2) + 1, N)

        if 1 < f1 < N:
            factors.add(f1)
        if 1 < f2 < N:
            factors.add(f2)

    return list(factors)

