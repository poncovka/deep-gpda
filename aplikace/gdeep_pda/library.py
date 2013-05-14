'''
Obsahuje ruzne funkce a tridy.

@author: Vendula Poncova
'''

import sys
from codecs import open
from .error import EPARAM, EIO, check


DEBUG = False
DEBUG_CODE = "[LIB]"

#=================================================================== enum()

def enum(*sequential, **named):
    
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

#=================================================================== isSurrounded()

def isSurrounded(item, left, right):
    
    if len(item) < 2 : return False
    else: return (item[0] == left and item[-1] == right)

#=================================================================== unquote()

def unquote(item, char = "'"):
    
    if isinstance(item, list) :
        
        for n,i in enumerate(item):
            item[n] = unquote(i)
                
    elif isinstance(item, str) :
        
        if isSurrounded(item, char, char) :
            item = item[1:-1]
            
    return item

#=================================================================== unquote()

def quote(item, group = None, char = "'"):
    
    if isinstance(item, list):
        
        for n,i in enumerate(item):
            item[n] = quote(i, group)
                
    elif isinstance(item, str) :
        
        if group == None or item in group :
            item = char + item + char
            
    return item

#=================================================================== tableprint()

def tableprint(table, head = False):
    check("Priprava tabulky.", DEBUG_CODE, DEBUG, level = 0)   
    
    # vypocet poctu radku a sloupcu a jejich velikosti
    nrow = 0
    ncolumn = 0
    size_columns = list()
    
    # spocitej radky
    for row in table:
        nrow += 1
        nitem = 0

        # pocitej sloupce
        for item in row :
            
            if len(size_columns) <= nitem :
                size_columns.append(len(item))
            else:
                size_columns[nitem] = max (size_columns[nitem], len(item))
                
            nitem += 1 
        
        # nastav velikost sloupce
        ncolumn = max(ncolumn, nitem)
    
    # vytvoreni tabulky        
    output = ""
    
    # prochazeni radku tabulky
    for row in table:
        
        # tisk polozek radku
        nitem = 0
        for item in row :
            
            output += (' {0:' + str(size_columns[nitem]) + '} ').format(item)
            nitem  += 1
            
        output += "\n"
        
        # tisk hlavicky tabulky
        if head :
            for n in range(0,ncolumn) :
                output +=  '-' * size_columns[n] + '--' 
                
            output += "\n"
            head = False
     
    # vrati retezec s tabulkou       
    return output

#=================================================================== printHelp()

def printHelp():
    msg = '''
    gdeep_pda: Redukce zobecneneho zasobnikoveho automatu
    Vendula Poncova (xponco00)

    gdeep_pda [-h|--help] [--input=filename] [--output=filename] [--reduce-states]
         [--reduce-symbols] [--analyze-string="string"]


    -h, --help                   Vypise napovedu.
    --input=filename             Nacte vstup ze souboru.
    --output=filename            Vypise vystup do souboru.
    --reduce-states              Zredukuje pocet stavu.
    --reduce-symbols             Zredukuje pocet nevstupnich symbolu.
    --analyze-string="string"    Zjisti, zda string je retezec jazyka prijimaneho
                                 danym automatem, a vypise sekvenci kroku.
                                 Jednotlive symboly musi byt oddelene mezerami.
    --max-steps=n                Analyza retezce se provede pro maximalne n
                                 derivacnich kroku pro n >= 0.
    \n'''
    sys.stdout.write(msg)

#=================================================================== processParams()

def processParams(argv):
    from .parser import GDPParser

    check("Zpracovani parametru.", DEBUG_CODE, DEBUG, level = 0)   

    arg_options = {"--input": "input", "--output": "output", 
                   "--analyze-string": "analyze_string", "--max-steps" : "max_steps" 
                  }

    flag_options = { "--help": "help", "-h": "help",
                     "--reduce-states": "reduce_states", 
                     "--reduce-symbols": "reduce_symbols"
                   }
    args = {} 

    # zpracovani parametru
    for arg in argv:
        opt, sep, value = arg.partition("=")

        if arg in flag_options and flag_options[arg] not in args:
            args[flag_options[arg]] = True

        elif opt in arg_options and arg_options[opt] not in args:
            args[arg_options[opt]] = value

        else: raise EPARAM("Chybne zadany parametr: " + arg)

    if ("help" in args) and len(args) != 1:
        raise EPARAM
        
    if "input" not in args :
        args["input"] = None

    if "output" not in args :
        args["output"] = None
        
    if "--reduce-symbols" in args and "--reduce-states" in args :
        raise EPARAM("Nelze volat oba parametry --reduce.")
        
    if "analyze_string" in args :
        string = GDPParser().parseString(args["analyze_string"])

        args["analyze_string"] = string
        check(string, DEBUG_CODE, DEBUG, level = 3)
    
    # defaultni hodnota
    if "max_steps" not in args :
        args["max_steps"] = 100
    
    # spatne zadane                
    elif "analyze_string" not in args :
        raise EPARAM("Ocekavan parametr --analyze-string.")
    
    # konverze z retezce
    else:
        try:
            args["max_steps"] = int(args["max_steps"])
            
            if args["max_steps"] < 0 : raise ValueError
            
        except ValueError :
            raise EPARAM("Chybna hodnota parametru --max-steps.")

    check(args, DEBUG_CODE, DEBUG, level = 2)
    return args

#=================================================================== readInput()

def readInput (filename):
    check("Nacteni vstupu.", DEBUG_CODE, DEBUG, level = 0)
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
        raise EIO("Chyba pri cteni souboru.")

    check(input, DEBUG_CODE, DEBUG, level = 2)
    return input

#=================================================================== readOutput()

def writeOutput(filename, output):
    check("Zapis vystupu.", DEBUG_CODE, DEBUG, level = 0)
    try:
        
        # zapis do souboru
        if filename != None :
            file = open(filename, mode='w', encoding='utf8')
            file.write(output)
            file.close()
        
            check(output, DEBUG_CODE, DEBUG, level = 2)
            
        # zapis na stdout
        else:
            file = sys.stdout.write(output)

    except IOError:
        raise EIO("Chyba pri zapisu do souboru.")


##################################################################### konec souboru