__author__ = 'Christopher Holder'
__maintainer_ = 'Christopher Holder'

from net import EthConnection

def main():
    con = EthConnection()
    con.run()
    print(str(con.web3.isConnected()))

if __name__ == '__main__':
    main()