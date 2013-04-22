'''
Aplikace pro redukci stavu nebo nevstupnich symbolu
zobecnenych hlubokych zasobnikovych automatu.

@author: Vendula Poncova
'''

from library import *
from parser import GDPParser


if __name__ == '__main__':
    print("Hello!")
    
    # zpracovani parametru
    args = processParams(sys.argv[1:])
    
    # vytisknuti napovedy
    if "help" in args:
        
        printHelp()
        exit(0)
    
    # nacteni vstupu
    input = readInput(args["input"])

    # nacteni automatu    
    automata = GDPParser().run(input)
    
    # vytiskne automat na vystup
    output = automata.serialize()
    writeOutput(args["output"], output)
    
    
    # konec
    exit(0)