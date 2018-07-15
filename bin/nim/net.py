"""
net.py - Manages the connections between the Ethereum Node and the program through
a Web3py wrapper.
"""
import time
import web3.eth
from web3 import Web3,HTTPProvider,IPCProvider
from web3.middleware import geth_poa_middleware
from hash import Key,hash,sha3

#TODO: Expand list of Ethereum network IDs.

netIds = {'main':1,'morden':2,'ropsten':3,'rinkeby':4,'kovan':42,'sokol':77,'core':99}
#TODO:Expand support and test other Eth networks.
#TODO: Disable key args for the EthConnection constructor.

class EthConnection:
    def __init__(self,type = 'infura',network='rinkeby',token ='n9LBfW1SzRzIjZfK5MfC'):
        self.__web3 = None
        self.type = type
        self.network = network
        self.token = token
        self.time = None
        self.__running =False
        self.__key = Key()
    #Connects to a node in a specific Ethereum network.
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

    #Alias to the () operator
    def run(self):
        if self.__call__():
            return True
        else:
            return False
    #Loads key from given path
    def loadKey(self,path):
        self.__key.load(path)
    #Decrypts keyfile(JSON) with
    def decryptKey(self,path,passphrase):
        self.__key.load(path)
        self.__key.decrypt(passphrase)

    #Displays key file
    def displayKeys(self):
        self.__key.display()

    #Signs an arbitrary string and returns a signature object
    def signMsg(self,msg):
        return self.__web3.eth.account.signHash(hash(msg), private_key=self.__key.getPrivate())

    #Input: Message Hash and signature.(Can be both Hex Strings or HexBytes)
    #Returns the address(Hex String) of the signee given a hash message and a hash signature
    def whoSign(self,msgHash,signature):
        return self.__web3.eth.account.recoverHash(msgHash, signature=signature)

    def signCheck(self,recipient, amount, nonce, contractAddress):
        sha3(["address", "uint256", "uint256", "address"],[recipient, amount, nonce, contractAddress])

    #Input : Hex String address(Could also be an ENS name)
    #Returns balance in ether(Decimal).
    def getBalance(self,address):
        return str(self.__web3.fromWei(self.__web3.eth.getBalance(address),'ether')) + ' Eth'

    #TODO: Add Ethereum Raw transactions support.
    #TODO: Extend support for gas price calculation strategies.

    def signTrans(self):
        print(str(Web3.eth.generateGasPrice()))