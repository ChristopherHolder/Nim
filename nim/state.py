"""
Author: Christopher Holder
nim.py - Main class implementations for the NIM prototype.
"""

#TODO: Use Numba JIT Compiler

from abc import abstractmethod,ABC


class StateChannel(ABC):
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def lock(self):
        pass

    @abstractmethod
    def unlock(self):
        pass

    @abstractmethod
    def kill(self):
        pass

class PaymentChannel(StateChannel):

    def start(self):
        #Deploy smart contract
        pass

    def lock(self):
        pass

    def unlock(self):
        pass

    def kill(self):
        pass


if __name__ == '__main__':
    pass