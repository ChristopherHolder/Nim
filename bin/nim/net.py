import time
from web3 import Web3,HTTPProvider
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
            else:
                self.web3 = Web3(HTTPProvider('http://localhost:8545'))
            self.time = time.asctime(time.localtime())
        except:
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

