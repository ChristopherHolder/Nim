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



def main():
    infura = Infura('rinkeby',token)
    infura.run()

    #msg = input('Message to sign: ')
    msg = 'hi'
    infura.decryptKey(path,'hola123')
    print(infura.address,end=' ')
    print(str(infura.getBalance(infura.address)))
    sign = infura.signStr(msg)
    print('Message hash: '+str(sign.messageHash))
    print('Signature: '+ str(sign.signature))
    print('Recover Hash : ',end='')
    signee = infura.whoSign(sign.messageHash,sign.signature)
    print(signee)
    print('Balance of account: '+str(infura.getBalance(signee)))
    print()


    #infura.send('0x030f7f7cc2689d4787a791501226680570d77372',0.01)

    #receiverPays.sol : 0x655b396f82826D9EbFCd79a993cdfD647cFEfF52
    #address = infura.deploy('receiverPays.sol',value=0.1)
    #print(infura.call(address,'greet'))

    other = Infura('rinkeby',token)
    other.run()
    other.decryptKey(path2,'hola123')
    check = Check(infura)
    #time.sleep(5)
    slip = check.write(other.address,0.02)
    print(other.address, end=' ')
    check2 = Check(other)
    print(str(other.getBalance(other.address)))
    check2.claimPayment(slip['address'],slip['amount'],slip['nonce'],slip['signature'])
    print(str(other.getBalance(other.address)))
if __name__ == '__main__':
    main()
