'''
    test-py - runs infrastructure and connection tests.
'''

import sys
import unittest
import logging
import time
import pprint

sys.path.insert(0,'../bin')

from net import Infura
from verifier import Check
from hash import soliditySha3
from web3 import Web3

solpath = '/home/abzu/PycharmProjects/Nim/res/solidity/'
token = 'n9LBfW1SzRzIjZfK5MfC'
newtoken = '9324c0d26478447aa2ccc26377e86dc7'
path = '/home/abzu/.ethereum/rinkeby/keystore/UTC--2018-06-29T15-24-00.421088464Z--7f039dee9c7d69db4009089d60b0eb5f355c3a81'
path2 = '/home/abzu/.ethereum/rinkeby/keystore/UTC--2018-07-23T14-16-06.281040785Z--030f7f7cc2689d4787a791501226680570d77372'

testType = 'fast'

class InfuraTest(unittest.TestCase):
    def setUp(self):
        self.A = Infura('rinkeby', newtoken)
        self.B = Infura('rinkeby', newtoken)
        self.assertTrue(self.A.run())
        self.assertTrue(self.B.run())
        self.A.decryptKey(path, 'hola123')
        self.B.decryptKey(path2, 'hola123')
        self.assertTrue(not self.A.isLock())
        self.assertTrue(not self.B.isLock())
    #@unittest.skip
    def test_hash(self):
        print('...test_hash()')
        #str = 'this is a test'

        #sign = self.A.signStr(str)
        #self.assertEqual(self.A.address, self.A.whoSign(sign.messageHash, sign.signature))
        ####

        #address = self.A.deploy('test3.sol')
        #a = self.B.call(address,'hash',4)[0]
        #b = soliditySha3(['uint256'], [4])
        #self.assertEqual(a, b)

        #a = self.B.call(address, 'hash3')[0]
        #print(a)
        
        #b = soliditySha3(['address'], [self.B.address])
        #b = self.B.address
        #print(b)
        #self.assertEqual(a, b)

    @unittest.skipIf(testType == 'fast','Reduces Ether in account and is slow.')
    def test_send(self):
        print('...Testing ether transactions.')
        amount = 0.2
        balA = self.A.getBalance()
        balB = self.B.getBalance()
        self.A.send(self.B.address, amount)
        balA2 = self.A.getBalance()
        balB2 = self.B.getBalance()
        self.assertTrue((float(balA2) + amount) < balA)
        self.assertTrue(balB2 > balB)
        print()

    @unittest.skipIf(testType == 'fast','Reduces Ether in account and is slow.')
    def test_deploy(self):
        #Checks that a contract can be deployed, tests whether a value can be attached.
        print('...test_deploy()')
        balA = self.A.getBalance()
        print('A: ' + str(balA) + ' ' + self.A.address)
        address = self.A.deploy('greeter.sol', 'hi', value=0.15)
        print('A deployed contract at ' + address)
        balA2 = self.A.getBalance()
        print('A: ' + str(balA2) + ' ' + self.A.address)
        self.assertTrue(type(address) == str)
        self.assertTrue((float(balA2) + 0.15) < balA)
        print()

    @unittest.skipIf(testType == 'fast', 'Reduces Ether in account and is slow.')
    def test_methods(self):
        print('...test_methods()')
        balA = self.A.getBalance()
        balB = self.B.getBalance()
        print('A: ' + str(balA) + ' ' + self.A.address)
        print('B: ' + str(balB) + ' ' + self.B.address)
        address = self.A.deploy('test.sol',  value=0.2)
        balA2 = self.A.getBalance()
        print('A: ' + str(balA2) + ' ' + self.A.address)
        print('A deployed contract at '+ address)
        self.assertTrue(float(balA2) + 0.2 < balA)
        self.B.call(address, 'getBalance',5)
        balB2 = self.B.getBalance()
        print('B called getBalance(5)')
        self.assertTrue((float(balB2) + 0.2) > balB)
        self.assertTrue(balB2 > balB)
        print('A: ' + str(balA2) + ' ' + self.A.address)
        print('B: ' + str(balB2) + ' ' + self.B.address)
        print()
    @unittest.skip
    def test_check(self):
        #TODO: Not sending full funds only a fraction.
        print('...test_check()')
        balA = self.A.getBalance()
        print('A: ' + str(balA) + ' ' + self.A.address)
        check = Check(self.A)
        check2 = Check(self.B)
        receipt = check.write(self.B.address, 0.2)
        balB = self.B.getBalance()
        print('B: ' + str(balB) + ' ' + self.B.address)
        print(receipt)
        slip = check2.claimPayment(receipt['address'], receipt['amount'], receipt['nonce'], receipt['signHexStr'])


        balB2 = self.B.getBalance()
        print('B: ' + str(balB2) + ' ' + self.B.address)

    @unittest.skip('Feature not ready for implementation')
    def test_check2(self):
        print('...Testing Checks 2')
        check = Check(self.A)
        balA = self.A.getBalance()
        time.sleep(10)
        print('A: ' + str(balA) + ' ' + self.A.address)
        check2 = Check(self.B)
        slip = check.write(self.B.address, 0.2)
        time.sleep(10)
        balA2 = self.A.getBalance()
        time.sleep(10)
        print('A: ' + str(balA2) + ' ' + self.A.address)
        self.assertTrue(balA2 < balA)
        balB = self.B.getBalance()
        time.sleep(10)
        print('B: ' + str(balB) + ' ' + self.B.address)
        print(slip)
        check2.claimPayment(slip['address'], slip['amount'], slip['nonce'], slip['signHexBytes'])
        time.sleep(10)
        balB2 = self.B.getBalance()
        time.sleep(10)
        print('B: ' + str(balB2) + ' ' + self.B.address)
        print(str(balB2) + ' > ' + str(balB) + '?')
        print(balB2 > balB)
        self.assertTrue(balB2 > balB)
        print()


if __name__ == '__main__':
    unittest.main()


def noUnitTest():
    A = Infura('rinkeby', token)
    B = Infura('rinkeby', token)
    A.decryptKey(path, 'hola123')
    B.decryptKey(path2, 'hola123')
    A.run()
    B.run()

    print('A: ' + str(A.getBalance()))
    print('B: ' + str(B.getBalance()))
    address = A.deploy('test.sol', 'a', 4, value=0.1)
    time.sleep(10)
    print('A.deploy(\'test.sol\',\'a\',4,value=0.1)')
    print('A: ' + str(A.getBalance()))
    print('B: ' + str(B.getBalance()))
    c = B.call(address, 'getBalance')
    print('B.call(address,\'getBalance\')')
    print('Result of call ' + str(c[0]))
    pprint.pprint(c[1])
    time.sleep(5)
    print('A: ' + str(A.getBalance()))
    print('B: ' + str(B.getBalance()))