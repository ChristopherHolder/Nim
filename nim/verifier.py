
'''
verifier.py - contains classes that represent common financial constructs
'''
import random
import json

from hash import soliditySha3,byte32,format
from web3 import Web3


class SimpleCheck:
    def __init__(self,connection):
        self.nonces = set()
        if connection.isRunning() and not connection.isLock():
            self.connection = connection

    def write(self,recipient,amount):
        '''

        :param recipient: Address of check recipient(HexString).
        :param amount: Amount in ether to be sent.(int)
        :return: json with
        '''
        self.address = self.connection.deploy('check.sol',price=4, value=amount)
        nonce = random.randrange(1,10000)
        print('Check deployed at: ' + self.address)
        amount = Web3.toWei(amount, 'ether')
        hash = byte32(soliditySha3(["address", "uint256","uint256","address"], [recipient, amount,nonce,self.address]))
        sign = format(self.connection.signHash(hash))
        check = {'address':self.address,'amount':amount,'nonce':nonce,'msgHash':sign[0],
                 'v':sign[1],'r':sign[2],'s':sign[3]}
        return json.dumps(check)
    def claim(self,json_file):
        check = json.loads(json_file)
        return self.connection.call(check['address'],'claim',check['amount'],check['nonce'],check['msgHash'],check['v'],check['r'],check['s'])[1]
    def kill(self):
        '''
        Must be contract creator.
        Executes contract termination
        '''
        self.connection.call(self.address,'kill')

