"""

hash.py - Holds the necessary wrapper classes to provide a simple but yet powerful array
of tools in dealing with private and public key operations.

eth_account - useful for key operations and account encryption without running an ethereum node.
"""
from eth_account import Account
import getpass

class Key:
    def __init__(self,path = None):
        if path != None:
            self.load(path)
        self.keyFile = ''
        self.__privateKey = None
        self.publicKey = None
        self.lock = None

    def load(self,path):
        if 'keystore' in path:
            with open(path) as keyfile:
                self.keyFile = str(keyfile.read())
                self.lock = True
            return True
        else:
            print('File path does not contain \' keystore \'')
            return False

    def isLock(self):
        return self.lock

    def decrypt(self,passphrase):
        if self.keyFile != None:
            try:
                self.__privateKey = Account.decrypt(self.keyFile,passphrase)
            except:
                print('Wrong passphrase')
                return False
            else:
                self.lock = False
                return True

    #TODO: To be implemented
    def encrypt(self,passphrase):
        pass

    def display(self):
        print('KeyFile (JSON): '+str(self.keyFile))
        #print('Private Key(HexBytes): '+str(self.__privateKey))

    def getPrivate(self):
        if self.lock == False:
            return self.__privateKey


if __name__ == '__main__':
    key = Key()
    key.load('/home/abzu/.ethereum/rinkeby/keystore/UTC--2018-06-29T15-24-00.421088464Z--7f039dee9c7d69db4009089d60b0eb5f355c3a81')
    key.decrypt(getpass.getpass())
    key.getAddress()
