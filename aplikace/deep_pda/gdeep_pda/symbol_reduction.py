'''
Created on 21.4.2013

@author: Vendula Poncova
'''

from pda import GDP

class SymbolReduction:
    '''
    Umoznuje redukci nevstupnich symbolu v GDP automatech.
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    def run(self, in_pda):
        '''
        Omezi pocet nevstupnich symbolu na tri
        '''
        out_pda = GDP()
        
        out_pda.Sigma = in_pda.Sigma
        