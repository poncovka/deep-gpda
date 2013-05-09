'''
Aplikace pro redukci stavu nebo nevstupnich symbolu
zobecnenych hlubokych zasobnikovych automatu.

@author: Vendula Poncova

Spusteni: python3 gdeep_pda params
'''

from .library import processParams, printHelp, readInput, writeOutput
from .parser import GDPParser
from .state_reduction import StateReduction
from .symbol_reduction import SymbolReduction
from .error import Error, EOK

import sys

##################################################################### run()

def run():
    
    try:
        
        # zpracovani parametru
        args = processParams(sys.argv[1:])
        
        # vytisknuti napovedy
        if "help" in args:
            
            printHelp()
            exit(EOK)
        
        # nacteni vstupu
        string = readInput(args["input"])
        
        # nacteni automatu    
        automata = GDPParser().run(string)
        
        # validace automatu
        automata.validate()
        
        # redukce stavu
        if "reduce_states" in args :
            automata = StateReduction().run(automata)
            
        # redukce nevstupnich symbolu
        elif "reduce_symbols" in args :
            automata = SymbolReduction().run(automata)
        
        # vytiskne automat na vystup
        output = automata.serialize()
        writeOutput(args["output"], output)
    
    # doslo ke zname chybe
    except Error as e :
        e.print()
        exit(e.code)
    
    # doslo k nezname chybe
    except Exception as e_unknown:
        
        e = Error(str(e_unknown))
        e.print()
        exit(e.code)
    
    # probehlo v poradku
    exit(EOK)
    
##################################################################### konec souboru