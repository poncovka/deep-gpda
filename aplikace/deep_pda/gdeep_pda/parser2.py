'''
Nacte z retezce zasobnikovy automat.
@author: Vendula Poncova
'''

import string

from library import check, error, enum, error_more
from pda import GDP

Tokens = enum('L_BRACKET','R_BRACKET',
              'L_CURLY', 'R_CURLY',
              'COMMA', 'ARROW',
              'STRING', 'STRING_A' )

class GDPScanner:
    '''
    Trida pro lexikalni analyzu GDP automatu.
    '''
    
    def __init__(self, input):
        
        self.input = input
        self.States = enum('BEGIN',
                           'L_BRACKET','R_BRACKET',
                           'L_CURLY', 'R_CURLY',
                           'COMMA',
                           'ARROW_DASH', 'ARROW',
                           'STRING',
                           'APOSTROPHE', 'STRING_A',
                           'COMMENT_SLASH', 'COMMENT',
                           )
        
    def getNextToken(self):
        return self.run()
    
    def getSymbol(self):
        return self.symbol
    
    def run(self):
        
        check("Lexikalni analyza")
              
        # nastaveni stavu a pomocneho retezce
        self.state = self.States.BEGIN
        self.symbol = ""
        
        index = 0
        
        # pro kazdy znak na vstupu
        while index < len(self.input) :
            
            char = self.input[index]
            
            if self.state == self.States.BEGIN :
                check("Pocatecni stav.")
                
                if char == '(' :
                    yield Tokens.L_BRACKET
                    
                elif char == ')' :
                    yield Tokens.R_BRACKET

                elif char == '{' :
                    yield Tokens.L_CURLY
                    
                elif char == '}' :
                    yield Tokens.R_CURLY
                    
                elif char == ',' :
                    yield Tokens.COMMA

                elif char == '-' :
                    self.symbol += char
                    self.state = self.States.ARROW_DASH
                    
                elif char == '/' :
                    self.symbol += char
                    self.state = self.States.COMMENT_SLASH
                    
                elif char == "'" :
                    self.symbol += char
                    self.state = self.States.APOSTROPHE

                elif char in string.whitespace:
                    pass
                
                elif char in string.printable:
                    self.symbol += char
                    self.state = self.States.STRING
                    
                else :
                    error_more("Lexikalni chyba: znak " + str(char))
                    
            elif self.state == self.States.ARROW_DASH :
                
                if char == '>' :
                    yield Tokens.ARROW
                    
                    self.symbol = ''
                    self.state = self.States.BEGIN

                else:
                    error_more("Lexikalni chyba: ocekavan > ,znak " + str(char))
                    
            elif self.state == self.States.COMMENT_SLASH :
                
                if char == '/' :
                    self.state = self.States.COMMENT
                else:
                    error_more("Lexikalni chyba: ocekavan /, znak " + str(char))
                    
            elif self.state == self.States.COMMENT :
                
                if char == "\n" :
                    self.symbol = ''
                    self.States.BEGIN
                    
                else :
                    pass
                
            elif self.state == self.States.STRING :
                
                if char in string.whitespace or char in "-,}" : 
                    pass
                if char in string.whitespace or char not in string.printable or char in "-,}" : 
                    pass
                    
            
        
        
        yield "ahoj"


class GDPParser:
    '''
    Parser pro nacteni GDP automatu z retezce.
    '''

    def __init__(self):
        '''
        Constructor
        '''

    def run(self, string):
        '''
        Nacteni PDA z retezce.
        '''
        check("Parsovani.")
        
        scanner = GDPScanner(string)
        check(scanner.getNextToken())

        # vytvoreni noveho automatu
        pda = GDP()
        

        # vrati nacteny automat
        check(pda)
        return pda
