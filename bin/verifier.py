#Not meant to be used. Not complete.

import random

from hash import soliditySha3,byte32
from web3 import Web3

class Check:
    def __init__(self,connection):
        if connection.isRunning() and not connection.isLock():
            self.connection = connection
    def signCheck(self, recipient, amount, nonce, contractAddress):
        amount = Web3.toWei(amount,'ether')
        hash = soliditySha3(["address", "uint256", "uint256", "address"], [recipient, amount, nonce, contractAddress])
        return {'signHexBytes':self.connection.signHash(hash).signature,
                'signHexStr':Web3.toHex(self.connection.signHash(hash).signature),
                'nonce':nonce, 'amount':amount, 'address':contractAddress, 'hash': hash
                ,'hashNum':Web3.toInt(hash)}

    def write(self,recipient,amount):
        '''
            As more optimized versions of the cheque contract are created.
            These will probably replace the programtheblockchain.com test2.sol
            example.
        '''
        address = self.connection.deploy('test2.sol',price=4, value=amount)
        print('Check deployed at: ' + address)
        nonce = random.randrange(1,100000)
        return self.signCheck(recipient,amount,nonce,address)

    def claimPayment(self,address,amount,nonce,signature):
        '''

        :param address:
        :param amount:
        :param nonce:
        :param signature:
        :return:
        '''
        receipt = self.connection.call(address,'claimPayment',amount,nonce,signature)
        return receipt[0]

    def kill(self):
        '''
        Must be contract creator.
        Executes contract termination
        '''
        self.connection.call(self.address,'kill')

