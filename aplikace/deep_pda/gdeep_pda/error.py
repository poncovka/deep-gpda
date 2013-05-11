'''
Definice vyjimek.

@author: Vendula Poncova
'''

import sys

##################################################################### DEBUG

# uroven pomocnych vypisu: 
# 0 - dulezite funkce, 1 - ostatni funkce, 2 - vypis dulezitych hodnot, 3 - pomocny vypis 

DEBUG = True
DEBUG_LEVEL = 0

def check(msg, code = "[DEBUG]", allowed = True, level = 0):
    '''Funkce pro kontrolni vypisy.'''
    
    if (DEBUG and allowed and level <= DEBUG_LEVEL) or (DEBUG and level == 0):
        sys.stderr.write("--- " + code + " " + str(msg) + "\n")

##################################################################### ERROR

EOK = 0

class Error(Exception):
    '''
    Zakladni trida pro vyjimky v modulu gdeep_pda.
    '''
    
    code = -1
    id   = "ERROR"
    msg  = "Pri behu aplikace doslo chybe. "
    
    def __init__(self, msg = None):
        
        if msg != None :
            self.msg = msg
    
    def __str__(self):
        return str( self.id + ": " + self.msg) 
    
    def print(self):
        sys.stderr.write(str(self) + "\n")
    
class EPARAM(Error):
    '''
    Vyjimka pro zpracovani parametru.
    '''
        
    code = 1
    id   = "EPARAM"
    msg = "Chybne zadane parametry. "
    
class EIO(Error):
    '''
    Vyjimka pro zpracovani parametru.
    '''
        
    code = 2
    id   = "EIO"
    msg = "Doslo k chybe pri praci se souborem. "
    
class EPDA(Error):
    '''
    Vyjimka pro zpracovani parametru.
    '''
        
    code = 3
    id   = "EDPA"
    msg = "Spatne zadany automat."

        