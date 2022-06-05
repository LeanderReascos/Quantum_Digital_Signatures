from libs.utils import swap_test, execute_circuit, basis_states_probs, intracircuit_teleportation
from libs.quantum_keyGenerator import pkey_generator, quantum_random
from qiskit import QuantumCircuit, ClassicalRegister , QuantumRegister, Aer, transpile
import numpy as np

class Alice:
    def __init__(self,n,L):
        self.n = n
        self.N = int(2**n)
        self.L = L
        f = lambda s: int(s,2)
        self.SK = np.array([list(map(f,quantum_random(n,L))),list(map(f,quantum_random(n,L)))])
        self.qr = QuantumRegister(2)
        self.cr = ClassicalRegister(2)
        self.b = int(quantum_random(1,1)[0])
    
    def prepare_state(self,qc:QuantumCircuit,i):
        sk0 = self.SK[0,i]
        sk1 = self.SK[1,i]
        self.i = i
        qc = qc.compose(pkey_generator(sk0,self.N),[self.qr[0]])
        qc = qc.compose(pkey_generator(sk1,self.N),[self.qr[1]])
        return qc
    
    def send_pubKeys(self,qc,B):
        qc = intracircuit_teleportation(qc,self.qr[0],B.qr[0],self.cr[0])
        qc = intracircuit_teleportation(qc,self.qr[1],B.qr[1],self.cr[1])
        return qc
    
    def send_signedMessage(self,B):
        B.receive_signedMessage(self.b,self.SK[self.b,self.i])

class Bob:
    def __init__(self,n):
        self.N = int(2**n)
        self.qr = QuantumRegister(3)
        self.Ancila = QuantumRegister(1)
        self.ancila = ClassicalRegister(1)
    
    def receive_signedMessage(self,b,s):
        self.b = b
        self.s = s

    def prepare_state(self,qc:QuantumCircuit):
        qc = qc.compose(pkey_generator(self.s,self.N),[self.qr[2]])
        return qc
    
    def verify_pk(self,qc):
        qc = swap_test(qc,[self.qr[self.b]],[self.qr[2]],self.Ancila,self.ancila)
        probs = basis_states_probs(execute_circuit(qc,shots=1))
        return np.sum(probs[:2**3//2])

class QDS:
    def __init__(self,n,L):
        self.Alice = Alice(n,L)
        self.Bob = Bob(n)
        self.L = L
    
    def create_quantumChanel(self):
        Ancila = self.Bob.Ancila
        alice = self.Alice.cr
        ancila = self.Bob.ancila
        qc = QuantumCircuit(self.Alice.qr,self.Bob.qr,Ancila,alice,ancila)
        return qc

    def protocol(self):
        results = []
        for i in range(self.L):
            qc =self.create_quantumChanel()
            qc = self.Alice.prepare_state(qc,i)
            qc = self.Alice.send_pubKeys(qc,self.Bob)
            self.Alice.send_signedMessage(self.Bob)
            qc = self.Bob.prepare_state(qc)
            results.append(self.Bob.verify_pk(qc)) 
        print()
        print(np.sum(results)/self.L)
    
qds = QDS(10,20)
qds.protocol()