#Not meant to be used. Not complete.

from hash import soliditySha3,byte32
from web3 import Web3

import json
import random
import sqlite3

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
        hash = soliditySha3(["address", "uint256", "uint256", "address"], [recipient, amount, nonce, contractAddress])
        return {'signHexBytes':self.connection.signMsg(hash).signature,
                'signHexStr':byte32(self.connection.signMsg(hash).signature),
                'nonce':nonce,'amount':amount,'address':contractAddress}

    def write(self,recipient,amount):
        self.__deploy(amount)
        nonce = random.randrange(1,100000)
        return self.__signCheck(recipient,amount,nonce,self.address)

    def claimPayment(self,address,amount,nonce,signature):
        receipt = self.connection.call(address,'claimPayment',amount,nonce,signature)
        print(receipt[1])

    def kill(self):
        '''
        Must be contract creator.
        Executes contract termination
        '''
        self.connection.call(self.address,'kill')

def notUnitTest():
    '''
        connectionA = Infura('rinkeby', token)
        connectionA.run()
        connectionB = Infura('rinkeby', token)
        connectionB.run()
        bal = connectionA.getBalance
        connectionA.decryptKey(path, 'hola123')
        connectionB.decryptKey(path2, 'hola123')
        check = Check(connectionA)
        balA = bal(connectionA.address)
        check2 = Check(connectionB)
        slip = check.write(connectionB.address, 0.2)
        balA2 = bal(connectionA.address)
        print(balA2 < balA)
        balB = bal(connectionB.address)
        print(slip)
        connectionB.call(slip['address'],'kill')
        balB2 = bal(connectionB.address)
        print(str(balB2) + ' > '+ str(balB) + '?' )
        print(balB2 > balB)
        '''