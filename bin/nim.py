"""
Author: Christopher Holder
nim.py - Main class implementations for the NIM prototype.
"""
#TODO: Add more logging support
#TODO: Use Numba JIT Compiler

import json
import random
import sqlite3

from abc import abstractmethod,ABC
from hash import sha3,byte32
from web3 import Web3

class Check:
    def __init__(self,connection):
        if connection.isRunning() and not connection.isLock():
            self.connection = connection
    def __deploy(self,amount):
        '''
        As more optimized versions of the cheque contract are created.
        These will probably replace the sample receiverPays.sol .
        '''
        self.address = self.connection.deploy('receiverPays.sol',value=amount)
        print('Contract Address: '+self.address)
    def __signCheck(self, recipient, amount, nonce, contractAddress):
        amount = Web3.toWei(amount,'ether')
        hash = sha3(["address", "uint256", "uint256", "address"], [recipient, amount, nonce, contractAddress])
        return {'signature':self.connection.signMsg(hash).signature,'nonce':nonce,'amount':amount,'address':contractAddress}

    def write(self,recipient,amount):
        self.__deploy(amount)
        nonce = random.randrange(1,100000)
        return self.__signCheck(recipient,amount,nonce,self.address)

    def claimPayment(self,address,amount,nonce,signature):
        result = self.connection.call(address,'claimPayment',amount,nonce,signature)
        print(result[1])

    def kill(self):
        '''
        Must be contract creator.
        Executes contract termination
        '''
        self.connection.call(self.address,'kill')

class StateChannel(ABC):
    @abstractmethod
    def connect(self):
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


if __name__ == '__main__':
    pass