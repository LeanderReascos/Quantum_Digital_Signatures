from libs.utils import swap_test, execute_circuit, basis_states_probs, intracircuit_teleportation
from libs.quantum_keyGenerator import pkey_generator, quantum_random
from qiskit import QuantumCircuit, ClassicalRegister , QuantumRegister, Aer, transpile
import numpy as np
from multiprocessing import Process

class Alice:
    def __init__(self,n,M):
        self.n = n
        self.N = int(2**n)
        self.M = M
        f = lambda s: int(s,2)
        self.SK = np.array([list(map(f,quantum_random(n,M))),list(map(f,quantum_random(n,M)))])
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
        B.receive_signedMessage(self.b,self.SK[self.b,self.i],self.n)

class Bob:
    def __init__(self,n,M):
        self.M = M
        self.qr = QuantumRegister(3)
        self.Ancila = QuantumRegister(1)
        self.ancila = ClassicalRegister(1)
        G = 2**-(n-1)
        self.c2M = (1-0.9**2)*(M-G)
        self.c1 = 0.05
        print(f'c1M: {self.c1*M} c2M: {self.c2M}')
    
    def receive_signedMessage(self,b,s,n):
        self.N = int(2**n)
        self.b = b
        self.s = s

    def prepare_state(self,qc:QuantumCircuit):
        qc = qc.compose(pkey_generator(self.s,self.N),[self.qr[2]])
        return qc
    
    def verify_pk(self,qc):
        qc = swap_test(qc,[self.qr[self.b]],[self.qr[2]],self.Ancila,self.ancila)
        probs = basis_states_probs(execute_circuit(qc,shots=1))
        return np.sum(probs[:2**3//2])

    def verify(self,r):
        if r <= self.c1*self.M:
            print(r,'1-ACC')
            return True
        if r > self.c1*self.M and r < self.c2M:
            print(r,'0-ACC')
            return True
        if r >= self.c2M:
            print(r,'REJ')
            return False
        

class QDS:
    def __init__(self,n,M):
        self.Alice = Alice(n,M)
        self.Bob = Bob(n,M)
        self.M = M
    
    def create_quantumChaneM(self):
        Ancila = self.Bob.Ancila
        alice = self.Alice.cr
        ancila = self.Bob.ancila
        qc = QuantumCircuit(self.Alice.qr,self.Bob.qr,Ancila,alice,ancila)
        return qc

    def protocoM(self):
        results = []
        for i in range(self.M):
            qc =self.create_quantumChaneM()
            qc = self.Alice.prepare_state(qc,i)
            qc = self.Alice.send_pubKeys(qc,self.Bob)
            self.Alice.send_signedMessage(self.Bob)
            qc = self.Bob.prepare_state(qc)
            results.append(self.Bob.verify_pk(qc)) 
        errors = self.M-np.sum(results)
        self.Bob.verify(errors)

if __name__ == '__main__':
    qds = QDS(20,30)
    qds.protocoM()