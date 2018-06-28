#Runs infraestructure and connection tests.

import sys
sys.path.insert(0,'../bin/nim')
import net

if __name__ == '__main__':
    try:
        con = net.EthConnection()
        assert con()
    except AssertionError as e:
        print(e,'Fail connection test')
