'''
Aplikace pro redukci stavu nebo nevstupnich symbolu
zobecnenych hlubokych zasobnikovych automatu.

@author: Vendula Poncova

Spusteni: python3 gdeep_pda params
'''

import sys
from .application import main

if __name__ == '__main__':
    main(sys.argv)