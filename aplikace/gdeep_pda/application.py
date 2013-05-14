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
from .error import Message, Error, EOK

##################################################################### run()

def main(argv):
    
    try:
        
        # zpracovani parametru
        args = processParams(argv[1:])
        
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
        
        # analyza retezce
        if "analyze_string" in args :
            
            string = args["analyze_string"]
            steps  = args["max_steps"]
            
            result, derivation = automata.analyze(string, steps)
            
            # pokud probehlo v poradku, vypise na vystup derivaci retezce
            if result :
                writeOutput(args["output"], derivation)
                
            # jinak vypise na stderr hlasku
            else :
                output = "Retezec '" +" ".join(string) + "' neni retezcem jazyka prijimaneho konecnym automatem. "
                output+= "Maximalni pocet kroku derivace je nastaven na: " + str(args["max_steps"])
                
                Message(output).print()

        # serializace automatu a vypis na vystup
        else :
            output = automata.serialize()
            writeOutput(args["output"], output)
    
    # doslo ke zname chybe
    except Error as e :
        e.print()
        exit(e.code)
    
#     # doslo k nezname chybe
#     except Exception as e_unknown:
#         
#         e = Error(str(e_unknown))
#         e.print()
#         exit(e.code)
    
    # probehlo v poradku
    exit(EOK)
    
##################################################################### konec souboru