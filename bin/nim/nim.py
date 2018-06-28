"""
nim.py - Main file of the Project Nim prototype.
"""
__author__ = 'Christopher Holder'
__maintainer_ = 'Christopher Holder'

from net import EthConnection

def main():
    eth = EthConnection()
    eth.run()





if __name__ == '__main__':
    main()