#Runs infraestructure and connection tests.

import sys
import time
import timeit
import unittest
from web3 import Web3
sys.path.insert(0,'../bin')

from net import Infura
from nim import Check
token = 'n9LBfW1SzRzIjZfK5MfC'
path = '/home/abzu/.ethereum/rinkeby/keystore/UTC--2018-06-29T15-24-00.421088464Z--7f039dee9c7d69db4009089d60b0eb5f355c3a81'
path2 = '/home/abzu/.ethereum/rinkeby/keystore/UTC--2018-07-23T14-16-06.281040785Z--030f7f7cc2689d4787a791501226680570d77372'
#TODO: Actual test should check for actual transactions.


class InfuraTest(unittest.TestCase):
    def setUp(self):
        self.connectionA = Infura('rinkeby',token)
        self.connectionB = Infura('rinkeby',token)
        self.bal = self.connectionA.getBalance
        self.assertTrue(self.connectionA.run())
        self.assertTrue(self.connectionB.run())
        self.connectionA.decryptKey(path, 'hola123')
        self.connectionB.decryptKey(path2,'hola123')
        self.assertTrue(not self.connectionA.isLock())
        self.assertTrue(not self.connectionB.isLock())
    def test_hash(self):
        str = 'this is a test'
        sign = self.connectionA.signStr(str)
        self.assertEqual(self.connectionA.address,self.connectionA.whoSign(sign.messageHash,sign.signature))
    def test_send(self):
        amount = 0.1
        balA = self.bal(self.connectionA.address)
        balB = self.bal(self.connectionB.address)
        self.connectionA.send(self.connectionB.address,amount)
        balA2 = self.bal(self.connectionA.address)
        balB2 = self.bal(self.connectionB.address)
        self.assertTrue(balA2 < balA)
        self.assertTrue(balB2 > balB)
    '''
    def test_check(self):
        check = Check(self.connectionA)
        check2 = Check(self.connectionB)
        checkAmount  = 0.2
        balA = self.bal(self.connectionA.address)
        balB = self.bal(self.connectionB.address)
        print('A: ' + str(balA) + ' ' + self.connectionA.address)
        print('B: ' + str(balB) + ' ' + self.connectionB.address)
        slip = check.write(self.connectionB.address,checkAmount)

        check2.claimPayment(slip['address'],slip['amount'],slip['nonce'],slip['signature'])
        balA2 = self.bal(self.connectionA.address)
        balB2 = self.bal(self.connectionB.address)

        #Check that contract deployment transaction reduces available ether.
        self.assertTrue(balA2 < balA)

        #Check that new account has received the ether deployed by the check contract
        #self.assertTrue(balB2 > balB)
        print('A: ' + str(balA2) + ' ' + self.connectionA.address)
        print('B: ' + str(balB2) + ' ' + self.connectionB.address)
    '''
if __name__ == '__main__':
    unittest.main()
