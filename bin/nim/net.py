"""
net.py - Manages the connections between the Ethereum Node and the program through
a Web3py wrapper.
"""
import time
import json
from web3 import Web3,HTTPProvider,IPCProvider
from web3.middleware import geth_poa_middleware

class EthConnection:
    def __init__(self,type = 'infura',network='rinkeby',token ='n9LBfW1SzRzIjZfK5MfC'):
        self.web3 = None
        self.type = type
        self.network = network
        self.token = token
        self.time = None
    def __call__(self, *args, **kwargs):
        try:
            if self.type == 'infura':
                self.web3 = Web3(HTTPProvider('https://' + self.network + '.infura.io/'+self.token))
                if self.network == 'rinkeby':
                    self.web3.middleware_stack.inject(geth_poa_middleware, layer=0)
            elif self.type == 'local' or self.type =='ipc':
                self.web3 = Web3(IPCProvider())
            self.time = time.asctime(time.localtime())
        except:
            # TODO: Deal with the specific exceptions.
            print('Connection Error')
            return False
        else:
            print('...Connection established with the ' + self.network + ' Ethereum network')
            if self.web3.isConnected():
                print('...Active connection at : ' + self.time)
                return True
    def run(self):
        if self.__call__():
            return True
        else:
            return False

