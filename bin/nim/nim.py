"""
nim.py - Main file of the Project Nim prototype.
"""
__author__ = 'Christopher Holder'
__maintainer_ = 'Christopher Holder'

import subprocess
import getpass

from net import EthConnection


def main():
    eth = EthConnection()
    eth.run()
    path = '/home/abzu/.ethereum/rinkeby/keystore/UTC--2018-06-29T15-24-00.421088464Z--7f039dee9c7d69db4009089d60b0eb5f355c3a81'
    msg = input('Message to sign: ')

    eth.loadKey(path)
    eth.decryptKey(getpass.getpass())

    hash = eth.hash(msg)
    sign = eth.signMsg(msg)
    print('Message hash: ' + str(hash))
    print('Message hash in signature object: '+str(sign.messageHash))
    print('Signature: '+ str(sign.signature))




if __name__ == '__main__':
    main()