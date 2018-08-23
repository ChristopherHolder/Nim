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
from web3 import Web3



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
    @unittest.skip
    def test_hash(self):
        print('...Testing hashing capabilities.')
        str = 'this is a test'
        sign = self.A.signStr(str)
        self.assertEqual(self.A.address, self.A.whoSign(sign.messageHash, sign.signature))

    @unittest.skipIf(testType == 'fast','Reduces Ether in account and is slow.')
    def test_send(self):
        logging.info('...Testing ether transactions.')
        amount = 0.2
        balA = self.A.getBalance()
        #time.sleep(2)
        balB = self.B.getBalance()
        #time.sleep(2)
        self.A.send(self.B.address, amount)
        #time.sleep(2)
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
        #time.sleep(2)
        print('A: ' + str(balA) + ' ' + self.A.address)
        address = self.A.deploy('greeter.sol', 'hi', value=0.15)
        print('A deployed contract at ' + address)
        #time.sleep(2)
        balA2 = self.A.getBalance()
        #time.sleep(2)
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
        #time.sleep(3)
        balA2 = self.A.getBalance()
        #time.sleep(2)
        print('A: ' + str(balA2) + ' ' + self.A.address)
        #time.sleep(2)
        print('A deployed contract at '+ address)
        self.assertTrue(float(balA2) + 0.2 < balA)
        self.B.call(address, 'getBalance',5)
        #time.sleep(2)
        balB2 = self.B.getBalance()
        print('B called getBalance(5)')
        self.assertTrue((float(balB2) + 0.2) > balB)
        self.assertTrue(balB2 > balB)
        print('A: ' + str(balA2) + ' ' + self.A.address)
        print('B: ' + str(balB2) + ' ' + self.B.address)
        print()
    #@unittest.skip
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
        print(str(int(slip[0])) + '   ' + str(int(slip[1])))

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