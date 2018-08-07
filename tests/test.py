#Runs infraestructure and connection tests.

import sys
import time
import timeit
import unittest

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
        self.assertTrue(self.connectionA.run())
        self.assertTrue(self.connectionB.run())
        self.assertTrue(self.connectionA.decryptKey(path, 'hola123'))
        self.assertTrue(self.connectionB.decryptKey(path2,'hola123'))
    def test_hash(self):
        str = 'this is a test'
        sign = self.connectionA.signStr(str)
        self.assertEqual(self.connectionA.address,self.connectionA.whoSign(sign.messageHash,sign.signature))
    def test_check(self):
        check = Check(self.connectionA)
        check2 = Check(self.connectionB)

        slip = check.write(self.connectionB.address,0.3)
        balA = self.connectionA.getBalance(self.connectionA.address)
        balB = self.connectionB.getBalance(self.connectionB.address)
        check2.claimPayment(slip['address'],slip['amount'],slip['nonce'],slip['signature'])
        balA2 = self.connectionA.getBalance(self.connectionA.address)
        balB2 = self.connectionB.getBalance(self.connectionB.address)

        #Check that contract deployment transaction reduces available ether.
        self.assertTrue(balA2 < balA)

        #Check that new account has received the ether deployed by the check contract
        self.assertTrue(balB2 > balB)

if __name__ == '__main__':
    unittest.main()
