"""
eth.py - Manages the connections between the Ethereum Node and the program through
a Web3py wrapper.
"""
import time
import sqlite3
import pickle
import datetime
import logging


from solc import compile_source
from web3 import Web3,HTTPProvider,IPCProvider,middleware
from web3.middleware import geth_poa_middleware
from hash import Key,byte32,hash


solpath = '/home/abzu/PycharmProjects/Nim/res/solidity/'

netIds = {'main':1,'morden':2,'ropsten':3,'rinkeby':4,'kovan':42,'sokol':77,'core':99}

#TODO: Generalize all file paths.
#TODO: Expand list of Ethereum network IDs.
#TODO:Expand support and test other Eth networks.
#TODO: Create custom exceptions.
#TODO: Add appropiate gas price recalculation. Connecting to eth gas station.


class Connection:
    '''
    Base class for the different type of connections with the Ethereum network.
    Not meant to be instantiated by itself.
    '''
    def __init__(self,type,network):
        self.type = type
        self.network = network
        self.running =False
        self.lock = True
        self.key = Key()
        self.conn = sqlite3.connect('../res/nim.db')
        self.c = self.conn.cursor()
        #self.c.execute('DROP TABLE Deployed')
        self.c.execute('CREATE TABLE IF NOT EXISTS Deployed (address STRING UNIQUE,filename STRING,contractObj BLOB,dat datetime)')
        self.conn.commit()

    def __call__(self, *args, **kwargs):
        try:
            if self.type == 'infura':
                self.web3 = Web3(HTTPProvider('https://' + self.network + '.infura.io/' + self.token))
                if self.network == 'rinkeby':
                    self.web3.middleware_stack.inject(geth_poa_middleware, layer=0)
            elif self.type == 'local' or self.type =='ipc':
                self.web3 = Web3(IPCProvider())
            self.time = time.asctime(time.localtime())
        except:
            logging.error('Connection Error')
            return False
        else:
            print('...Connection established with the ' + self.network + ' Ethereum network')
            logging.info('...Connection established with the ' + self.network + ' Ethereum network')
            if self.web3.isConnected():
                print('...Active connection at : ' + self.time)
                self.running = True
                return True


    #Alias to the () operator, and guarantees a boolean value.
    def run(self):
        if self.__call__():
            return True
        else:
            return False
    #Loads key from given path
    def isLock(self):
        return self.lock
    def isRunning(self):
        return self.running
    def loadKey(self,path):
        self.web3.eth.enable_unaudited_features()
        self.key.load(path)

    def decryptKey(self,path,passphrase):
        '''
        :param path: Path to keyfile.
        :param passphrase: Decrypts keyfile.
        :return: Decrypts keyfile(JSON) with passphrase.
        '''
        self.web3.eth.enable_unaudited_features()
        self.key.load(path)
        self.key.decrypt(passphrase)
        self.address = self.key.address
        self.lock = False
    def wait_for_receipt(self, tx_hash, poll_interval):
        '''
        :param tx_hash: Transaction hash(bytes?)
        :param poll_interval: Seconds to wait per in-between fetching.
        :return: Transaction Receipt.
        '''
        while True:
            tx_receipt = self.web3.eth.getTransactionReceipt(tx_hash)
            if tx_receipt:
                print('Transaction mined.')
                return tx_receipt
            print('...Pending')
            time.sleep(poll_interval)
    def signStr(self,s):
        '''
        :param s: String
        :return: Signature object of s
        '''
        return self.web3.eth.account.signHash(hash(s), private_key=self.key.getPrivate())

    def signMsg(self,msgHash):
        '''
        :param msgHash:
        :return: Signature object of the message hash.
        '''
        return self.web3.eth.account.signHash(msgHash, private_key=self.key.getPrivate())

    def whoSign(self,msgHash,signature):
        '''
        :param msgHash: Hashed message.
        :param signature: Hex String or Hex Bytes
        :return: Address of signer
        '''
        return self.web3.eth.account.recoverHash(msgHash, signature=signature)

    def getBalance(self,address):
        return self.web3.fromWei(self.web3.eth.getBalance(address), 'ether')

    def searchContract(self,filename):
        self.c.execute('SELECT address FROM Deployed WHERE filename = ? ORDER BY dat DESC',(filename,))
        data = self.c.fetchone()
        if data == None:
            print('Contract not deployed through Nim')
            return False
        return data[0]

class Infura(Connection):
    '''
    Child class to connection, customized for interaction with Infura nodes.
    '''
    def __init__(self,network,token):
        Connection.__init__(self,'infura', network)
        self.token = token

    def send(self, to, value, price=4):
        '''
        :param to: Hex string of payment receiver.
        :param value: Value in Ether
        :param price: Price of gas
        :return: Receipt of the transaction.
        '''

        # Gas estimation also depends on the specified ethereum network
        nonce = self.web3.eth.getTransactionCount(self.key.address)
        gas = self.web3.eth.estimateGas({'to': to, 'from': self.key.address, 'value': Web3.toWei(value, 'ether')})
        trans = {'to': to,'value': Web3.toWei(value, 'ether'),
                'gas': gas,'gasPrice': Web3.toWei(price, 'gwei'),
                'nonce': nonce,'chainId': netIds[self.network]}

        self.web3.eth.enable_unaudited_features()
        signObj = self.web3.eth.account.signTransaction(trans, self.key.getPrivate())
        return self.wait_for_receipt(byte32(self.web3.eth.sendRawTransaction(signObj.rawTransaction)), 10)


    def deploy(self, path, *arg, price=2, value=0):
        '''
        Deploys a solidity source file and returns the address of the contract.
        Also stores the serialized compile object on a sql database.
        '''
        # self.c.execute('SELECT address FROM Deployed WHERE address = ?', (contractAddress,))

        solname = path
        path = solpath + path
        f = open(path, 'r')
        compiled_sol = compile_source(f.read())
        f.close()
        contractName, contract_interface = compiled_sol.popitem()
        blob = pickle.dumps(contract_interface)
        bin, abi = contract_interface['bin'], contract_interface['abi']
        contract = self.web3.eth.contract(abi=abi, bytecode=bin)
        nonce = self.web3.eth.getTransactionCount(self.key.address)
        if arg == None:
            txn = contract.constructor().buildTransaction({'gasPrice': Web3.toWei(price, 'gwei')})
        else:
            txn = contract.constructor(*arg).buildTransaction({'gasPrice': Web3.toWei(price, 'gwei')})
        txn['nonce'] = nonce
        if value == 0:
            pass
        else:
            txn['value'] = Web3.toWei(value, 'ether')
        txn['chainId']= netIds[self.network]
        print(txn)
        self.web3.eth.enable_unaudited_features()
        signObj = self.web3.eth.account.signTransaction(txn, self.key.getPrivate())
        txnHash = byte32(self.web3.eth.sendRawTransaction(signObj.rawTransaction))
        address = self.wait_for_receipt(txnHash, 10)['contractAddress']
        entry = (address, solname, blob,datetime.datetime.now())
        self.c.execute('INSERT INTO Deployed(address,filename,contractObj,dat) VALUES (?,?,?,?)', entry)
        self.conn.commit()
        return address

    def call(self, contractAddress, methodName, *arg, price=4, value=0):
        '''
        Broadcasts a method call transaction to the network.
        :param contractAddress: HexString address of a contract deployed through Nim.
        #TODO: Let people load their own abi ?
        :param methodName: (string)
        :param arg: Respective arguments for the method
        :param price: (unsigned int) price in gwei for gas
        :param value: (ether)value for the transaction in ether.
        :return: tuple with locally calculated return value at [0] and transaction receipt at [1] for the method.
        '''
        self.c.execute('SELECT contractObj FROM Deployed WHERE address = ?', (contractAddress,))
        data = self.c.fetchone()
        if data == None:
            print('Contract not deployed through Nim.')
            return False
        interface = pickle.loads(data[0])
        contract = self.web3.eth.contract(abi=interface['abi'], bytecode=interface['bin'], address=contractAddress)
        if methodName not in contract.functions.__dict__.keys():
            print('Method not in contract')
            return False
        if methodName == 'fallback':
            func = contract.functions.fallback()
        else:
            func = contract.functions.__dict__[methodName]
        txn = func(*arg).buildTransaction({'nonce': self.web3.eth.getTransactionCount(self.key.address)})
        txn['gasPrice'] = Web3.toWei(price, 'gwei')
        txn['chainId'] = netIds[self.network]
        if value == 0:
            pass
        else:
            txn['value'] = Web3.toWei(value, 'ether')
        signObj = self.web3.eth.account.signTransaction(txn, self.key.getPrivate())
        txnHash = byte32(self.web3.eth.sendRawTransaction(signObj.rawTransaction))


        return (func(*arg).call(),self.wait_for_receipt(txnHash, 10))

