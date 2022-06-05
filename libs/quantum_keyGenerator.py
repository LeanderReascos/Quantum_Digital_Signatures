from qiskit import QuantumCircuit, QuantumRegister, Aer, transpile
from libs.utils import execute_circuit
import numpy as np

def quantum_random(n,m):
    qc = QuantumCircuit(n)
    [qc.h(i) for i in range(n)]
    qc.measure_all()
    counts = execute_circuit(qc,shots=m)
    results = list(zip(counts.keys(),counts.values()))
    return [c for (c,r) in results for _ in range(r)]

def pkey_generator(sk,N):
    qc = QuantumCircuit(1)
    theta = 4*np.pi*sk/N
    qc.ry(theta,0)
    return qc
        