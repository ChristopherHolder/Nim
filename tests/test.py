#Runs infraestructure and connection tests.

import sys,os,time
sys.path.insert(0,'../bin/nim')

from eth import Infura

token = 'n9LBfW1SzRzIjZfK5MfC'
path = '/home/abzu/.ethereum/rinkeby/keystore/UTC--2018-06-29T15-24-00.421088464Z--7f039dee9c7d69db4009089d60b0eb5f355c3a81'

def main():
    infura = Infura('rinkeby',token)
    infura.run()

    msg = input('Message to sign: ')
    infura.decryptKey(path,'hola123')

    sign = infura.signMsg(msg)
    print('Message hash: '+str(sign.messageHash))
    print('Signature: '+ str(sign.signature))
    print('Recover Hash : ',end='')
    signee = infura.whoSign(sign.messageHash,sign.signature)
    print(signee)
    print('Balance of account: '+str(infura.getBalance(signee)))

    infura.send('0x486F5A3F0EA8b237bf6B6b10C166ddF9e3041192',0.01)
    address = infura.deploy('greeter.sol','hey')

    print(infura.call('0x0939067C575923b5A5022e67eaDdd5D55E468D32','greet'))



if __name__ == '__main__':
    main()