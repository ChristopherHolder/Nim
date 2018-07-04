"""
net.py - Manages the connections between the Ethereum Node and the program through
a Web3py wrapper.
"""
import time
import json
from web3 import Web3,HTTPProvider,IPCProvider
from web3.middleware import geth_poa_middleware
from eth_account.messages import defunct_hash_message
from hash import Key

class EthConnection:
    def __init__(self,type = 'infura',network='rinkeby',token ='n9LBfW1SzRzIjZfK5MfC'):
        self.__web3 = None
        self.type = type
        self.network = network
        self.token = token
        self.time = None
        self.__running =False
        self.__key = Key()
    def __call__(self, *args, **kwargs):
        try:
            if self.type == 'infura':
                self.__web3 = Web3(HTTPProvider('https://' + self.network + '.infura.io/'+self.token))
                if self.network == 'rinkeby':
                    self.__web3.middleware_stack.inject(geth_poa_middleware, layer=0)
            elif self.type == 'local' or self.type =='ipc':
                self.__web3 = Web3(IPCProvider())
            self.time = time.asctime(time.localtime())
        except:
            # TODO: Deal with the specific exceptions.
            print('Connection Error')
            return False
        else:
            print('...Connection established with the ' + self.network + ' Ethereum network')
            if self.__web3.isConnected():
                print('...Active connection at : ' + self.time)
                return True
            self.__running = True
    def run(self):
        if self.__call__():
            return True
        else:
            return False

    def loadKey(self,path):
        self.__key.load(path)

    def decryptKey(self,passphrase):
        self.__key.decrypt(passphrase)

    def displayKeys(self):
        self.__key.display()


    # TODO: To be implemented
    def web3encrypt(self):
        pass

    # TODO: To be implemented
    def web3decrypt(self):
        pass

    def hash(self,msg):
        return defunct_hash_message(text=msg)

    def signMsg(self,msg):
        return self.__web3.eth.account.signHash(self.hash(msg), private_key=self.__key.getPrivate())

