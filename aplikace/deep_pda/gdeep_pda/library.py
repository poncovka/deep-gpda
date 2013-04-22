'''
Obsahuje ruzne funkce a tridy.

@author: Vendula Poncova
'''

import sys
from codecs import open

debug = True

errors = {"EPARAM": ("Spatne zadane parametry.", 1), 
          "EREAD": ("Chyba pri cteni ze souboru.", 2), 
          "EWRITE": ("Chyba pri zapise do souboru.", 3), 
          "EPDA": ("Chyba v definici pda.", 4),
          "ERROR": ("Doslo k chybe.", 5)
          }

def check(string):
    '''Funkce pro kontrolni vypisy.'''
    
    if debug:
        sys.stderr.write("========== " + str(string) + "\n")

def error(err):
    '''Vypise chybovou hlasku a skonci.'''
    
    (msg, code) = errors[err]
    
    sys.stderr.write("ERR: " + msg + "\n", )
    sys.exit(code)
    
def error_more(more):
    '''Vypise chybovou hlasku a skonci.'''
    
    (msg, code) = errors["ERROR"]
    
    sys.stderr.write("ERR: " + msg + " " + more + "\n", )
    sys.exit(code)

def printHelp():
    msg = '''
    gdeep_pda: Redukce zobecneneho zasobnikoveho automatu
    Vendula Poncova (xponco00)

    gdeep_pda [-h] [--input=filename] [--output=filename] [--reduce-states]
         [--reduce-symbols] [--analyze-string="string"]


    -h, --help                   Vypise napovedu.
    --input=filename             Nacte vstup ze souboru.
    --output=filename            Vypise vystup do souboru.
    --reduce-states              Zredukuje pocet stavu.
    --reduce-symbols             Zredukuje pocet nevstupnich symbolu.
    --analyze-string="string"    Zjisti, zda string je retezec jazyka prijimaneho
                                 danym automatem, a vypise sekvenci kroku.
    \n'''
    sys.stdout.write(msg)

def processParams(argv):

    check("Zpracovani parametru:")   

    arg_options = {"--input": "input", "--output": "output", "--analyze-string": "analyze_string"}

    bool_options = { "--help": "help", "-h": "help",
                     "--reduce-states": "reduce_states", 
                     "--reduce-symbols": "reduce_symbols",  
                   }
    args = {} 

    # zpracovani parametru
    for arg in argv:
        (opt, sep, value) = arg.partition("=")

        if arg in bool_options and bool_options[arg] not in args:
            args[bool_options[arg]] = True

        elif opt in arg_options and arg_options[opt] not in args:
            args[arg_options[opt]] = value

        else: error("EPARAM")

    if ("help" in args) and len(args) != 1:
        error("EPARAM")
        
    if "input" not in args :
        args["input"] = None

    if "output" not in args :
        args["output"] = None

    check(args)
    return args


def readInput (filename):
    check("Nacteni vstupu:")
    try:
        
        # cteni ze souboru
        if filename != None :
            
            file = open(filename, mode='r', encoding='utf8')
            input = file.read()
            file.close()
            
        # cteni ze stdin
        else:
            input = sys.stdin.read()

    except IOError:
        error("EREAD")

    check(input)
    return input

def writeOutput(filename, output):
    check("Zapis vystupu:")
    try:
        
        # zapis do souboru
        if filename != None :
            file = open(filename, mode='w', encoding='utf8')
            file.write(output)
            file.close()
        
            check(output)
            
        # zapis na stdout
        else:
            file = sys.stdout.write(output)

    except IOError:
        error("EWRITE")


# konec souboru library.py