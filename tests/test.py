#Runs infraestructure and connection tests.

import sys
sys.path.insert(0,'../bin/nim')

import getpass

from net import EthConnection


def main():
    eth = EthConnection()
    eth.run()
    path = '/home/abzu/.ethereum/rinkeby/keystore/UTC--2018-06-29T15-24-00.421088464Z--7f039dee9c7d69db4009089d60b0eb5f355c3a81'
    msg = input('Message to sign: ')

    eth.loadKey(path)
    eth.decryptKey('hola123')

    sign = eth.signMsg(msg)
    print('Message hash: '+str(sign.messageHash))
    print('Signature: '+ str(sign.signature))
    print('Recover Hash : ',end='')
    a = eth.whoSign(sign.messageHash,sign.signature)
    print(a)
    print('Balance of account: '+str(eth.getBalance(a)))


if __name__ == '__main__':
    main()