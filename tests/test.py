#Runs infraestructure and connection tests.

import sys
import time
import timeit
import unittest
import logging

sys.path.insert(0,'../bin')

from net import Infura
from nim import Check
solpath = '/home/abzu/PycharmProjects/Nim/res/solidity/'
token = 'n9LBfW1SzRzIjZfK5MfC'
path = '/home/abzu/.ethereum/rinkeby/keystore/UTC--2018-06-29T15-24-00.421088464Z--7f039dee9c7d69db4009089d60b0eb5f355c3a81'
path2 = '/home/abzu/.ethereum/rinkeby/keystore/UTC--2018-07-23T14-16-06.281040785Z--030f7f7cc2689d4787a791501226680570d77372'

testType = 'fast'

class InfuraTest(unittest.TestCase):
    def setUp(self):
        logging.info('')
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

    @unittest.skipIf(testType == 'fast','Reduces Ether in account and is slow.')
    def test_send(self):
        amount = 0.1
        balA = self.bal(self.connectionA.address)
        balB = self.bal(self.connectionB.address)
        self.connectionA.send(self.connectionB.address,amount)
        balA2 = self.bal(self.connectionA.address)
        balB2 = self.bal(self.connectionB.address)
        self.assertTrue((float(balA2) + amount) < balA)
        self.assertTrue(balB2 > balB)

    @unittest.skipIf(testType == 'fast','Reduces Ether in account and is slow.')
    def test_deploy(self):
        #Checks that a contract can be deployed, tests whether a value can be attached.

        balA = self.bal(self.connectionA.address)
        print('A: ' + str(balA) + ' ' + self.connectionA.address)
        address = self.connectionA.deploy('greeter.sol','hi',value=0.15)
        balA2 = self.bal(self.connectionA.address)
        print('A: ' + str(balA2) + ' ' + self.connectionA.address)
        self.assertTrue(type(address) == str)
        self.assertTrue((float(balA2) + 0.15) < balA)

    @unittest.skipIf(testType == 'fast', 'Reduces Ether in account and is slow.')
    def test_methods(self):
        balA = self.bal(self.connectionA.address)
        balB = self.bal(self.connectionB.address)
        print('A: ' + str(balA) + ' ' + self.connectionA.address)
        print('B: ' + str(balB) + ' ' + self.connectionB.address)
        address = self.connectionA.deploy('test.sol','hola',5,value=0.2)
        balA2 = self.bal(self.connectionA.address)
        print('A deployed contract ' + str(balA) + ' ' + self.connectionA.address)
        self.assertTrue(float(balA2) + 0.2 < balA)
        self.connectionB.call(address,'getBalance')
        balB2 = self.bal(self.connectionB.address)
        print('B called getBalance' + str(balB2) + ' ' + self.connectionB.address)
        self.assertTrue(float(balB2) > balB)

    @unittest.expectedFailure
    def test_check(self):
        check = Check(self.connectionA)
        check2 = Check(self.connectionB)
        checkAmount  = 0.2
        balA = self.bal(self.connectionA.address)
        balB = self.bal(self.connectionB.address)
        print('A: ' + str(balA) + ' ' + self.connectionA.address)
        print('B: ' + str(balB) + ' ' + self.connectionB.address)
        slip = check.write(self.connectionB.address,checkAmount)
        print(slip)
        check2.claimPayment(slip['address'],slip['amount'],slip['nonce'],slip['signature'])
        balA2 = self.bal(self.connectionA.address)
        balB2 = self.bal(self.connectionB.address)
        #time.sleep(130)
        #Check that contract deployment transaction reduces available ether.
        #self.assertTrue(float(balA2) + checkAmount < balA)

        #Check that new account has received the ether deployed by the check contract
        #self.assertTrue(balB2 > balB)
        print('A: ' + str(balA2) + ' ' + self.connectionA.address)
        print('B: ' + str(balB2) + ' ' + self.connectionB.address)


if __name__ == '__main__':
    unittest.main()
