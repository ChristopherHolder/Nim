"""
Author: Christopher Holder
nim.py - Main class implementations for the NIM prototype.
"""
# TODO: Use Flask to handle json requests.

import json

from abc import abstractmethod,ABC
from hash import sha3
from web3 import Web3

class Check:
    def __init__(self,connection):
        if connection.isRunning() and not connection.isLock():
            self.connection = connection
    def deploy(self):
        self.address = self.connection.deploy('receiverPays.sol')

    def signCheck(self, recipient, amount, nonce, contractAddress):
        amount = Web3.toWei(amount,'ether')
        hash = sha3(["address", "uint256", "uint256", "address"], [recipient, amount, nonce, contractAddress])
        return json.dumps({'signature':self.connection.signMsg(hash).signature,'nonce':nonce,'amount':amount})

    def claimPayment(self):
        pass

    def kill(self):
        self.connection.call('kill')

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



if __name__ == '__main__':
    pass