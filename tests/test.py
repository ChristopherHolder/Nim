#Runs infraestructure and connection tests.

import sys,os
sys.path.insert(0,'../bin/nim')

from eth import EthConnection



def main():
    infura = EthConnection()
    infura.run()
    #TODO: Should use a file explorer. Rather than hardcoding the path.
    path = '/home/abzu/.ethereum/rinkeby/keystore/UTC--2018-06-29T15-24-00.421088464Z--7f039dee9c7d69db4009089d60b0eb5f355c3a81'
    #msg = input('Message to sign: ')

    infura.decryptKey(path,'hola123')

    #sign = infura.signMsg(msg)
    #print('Message hash: '+str(sign.messageHash))
    #print('Signature: '+ str(sign.signature))
    #print('Recover Hash : ',end='')
    #signee = infura.whoSign(sign.messageHash,sign.signature)
    #print(signee)
    #print('Balance of account: '+str(infura.getBalance(signee)))

    #infura.send('0x486F5A3F0EA8b237bf6B6b10C166ddF9e3041192',0.01))
    #a = infura.checkMined('0x2df10817d9555547d6c58ccbee03ba6950d37ff4c1999c998d67e34aed729857')
    #print(a['blockHash'])
    # 0xa694bd52c8d73951b3cFC0ce069Ae7FB890ECFc4
    address = infura.deploy('greeter.sol','hey')
    #infura.call('0xa694bd52c8d73951b3cFC0ce069Ae7FB890ECFc4','greet')

if __name__ == '__main__':
    main()