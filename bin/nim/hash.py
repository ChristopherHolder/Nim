"""
hash.py - Holds the necessary wrapper classes to provide a simple but yet powerful array
of tools in dealing with private and public key operations.
"""
from eth_account import Account

class Key:
    def __init__(self,path = None):
        if path != None:
            self.load(path)
        self.keyFile = ''
        self.__privateKey = None
        self.publicKey = None
        self.encrypted = None

    def load(self,path):
        with open(path) as keyfile:
            self.keyFile = str(keyfile.read())
            self.encrypted = True

    def isEncrypted(self):
        return self.encrypted

    def decrypt(self,password):
        if self.keyFile != None:
            self.__privateKey = Account.decrypt(self.keyfile,password)
            # TODO: Add the due exceptions if password is not decrypted.
            self.encrypted = False
    def __str__(self):
        return self.keyFile
    def sign(self):
        pass


if __name__ == '__main__':
    key = Key()
    key.load('/home/abzu/.ethereum/keystore/UTC--2018-06-23T19-23-45.824667344Z--f07e32043e757a2a9870ae563d72984d4b1d7917')
    print(key.keyFile)