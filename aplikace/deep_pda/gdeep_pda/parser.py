'''
Nacte z retezce zasobnikovy automat.
@author: Vendula Poncova
'''

import re

from library import check, error
from pda import GDeepPDA

class GDPParser:
    '''
    Parser pro nacteni GDP automatu z retezce.
    '''

    def __init__(self):
        '''
        Constructor
        '''

        # regularni vyrazy popisujici definici pda

        self.pda_pattern = re.compile (r'''
        ^\s*\(
        \s*\{((?:'[^']*'|[^}{'])*)\}\s*,
        \s*\{((?:'[^']*'|[^}{'])*)\}\s*,
        \s*\{((?:'[^']*'|[^}{'])*)\}\s*,
        \s*\{((?:'[^']*'|[^}{'])*)\}\s*,
        \s*((?:'[^']*'|[^',])*)\s*,
        \s*((?:'[^']*'|[^',])*)\s*,
        \s*\{((?:'[^']*'|[^}{'])*)\}\s*
        \)\s*$
        ''', re.VERBOSE)

        self.symbol_pattern = re.compile (r'''
        ^\s*
        ((?:'(?:''|[^'])*'|[^-(){}\'<>,.|# \t\n]+))
        \s*
        ''', re.VERBOSE) 
        
        self.state_pattern = re.compile (r'''
        ^\s*
        ((?:'(?:''|[^'])+'|[^-(){}\'<>,.|# \t\n]+))
        \s*
        ''', re.VERBOSE)
        
        self.separator_pattern = re.compile (r'''
        ^\s*
        (->)
        \s*
        ''', re.VERBOSE)  
        
    def match(self, pattern, string):
        '''
        Aplikuje na retezec regularni vyraz
        a vrati vysledek.
        '''       
        # aplikuje regularni vyraz na retezec
        result = re.match(pattern, string)
        
        # nepovedlo se, chyba v zapise automatu
        if result == None:
            error("EPDA")
            
        # vrati vysledek
        return result
    
    def matchItems(self, pattern, string):
        '''
        Nacte z retezce polozky oddelene carkou
        '''
        
        items = set()
        
        start = 0
        end = len(string)
        comma = False
        
        # dokud neprojde cely retezec
        while start < end :
            
            # v retezci nasleduje oddelovac carka
            if comma:
                
                if string[start] == ',' :
                    start += 1
                    comma = False
                else :
                    error("EPDA")
            
            # v retezci ocekavame polozku        
            else:
                # aplikuje regularni vyraz na retezec
                result = self.match(pattern, string[start:])                
                # posune se ukazatel na retezec
                start += result.end()
                # nova polozka se ulozi
                items.add(result.groups()[0])
                # nastavi se indikator oddelovace
                comma = True
            
        # vrati prvky skupiny
        return items
    
    def matchItem(self, pattern, string):
        
        items = self.matchItems(pattern, string)
        return items.pop()
    
    def matchRules(self, string):
        '''
        Nacte pravidla z retezce
        '''
                
        rules = set()
        
        start = 0
        end = len(string)
        comma = False
       
        # dokud neprojde cely retezec
        while start < end :
            
            # v retezci nasleduje oddelovac carka
            if comma:
                
                if string[start] == ',' :
                    start += 1
                    comma = False
                else :
                    error("EPDA")
            
            # v retezci ocekavame pravidlo
            else:

                rule_left = list()
                rule_right = list()
                
                # parsuje polozky leve strany pravidla
                for pattern in (self.state_pattern, 
                                self.symbol_pattern,
                                self.separator_pattern,
                                self.state_pattern)     :
                    
                    # aplikuje regularni vyraz na retezec
                    result = self.match(pattern, string[start:])
                    # posune ukazatel retezce
                    start += result.end()
                    # ulozi polozku pravidla
                    rule_left.append(result.groups()[0])   
                
                # parsuje symboly na prave strane pravidla    
                while start < end and string[start] != ',' :
                    
                    # aplikuje regularni vyraz na retezec
                    result = self.match(self.symbol_pattern, string[start:])
                    # posune ukazatel retezce
                    start += result.end()
                    
                    # ulozi symbol pokud to neni prazdny retezec
                    if result.groups()[0] != "''" :
                        rule_right.append(result.groups()[0])            
                
                # nove pravidlo se ulozi
                rule = (rule_left[0], rule_left[1], rule_left[3], tuple(rule_right))
                rules.add(rule)
                
                # nastavi se indikator oddelovace
                comma = True
            
        # vrati mnozinu pravidel
        return rules

    def run(self, string):
        '''
        Nacteni PDA z retezce.
        '''
        check("Parsovani.")
        
        # smazani komentaru
        string = re.sub("(#.*)", " ", string)

        # vytvoreni noveho automatu
        pda = GDeepPDA()
        
        # parsovani automatu
        result = self.match(self.pda_pattern, string)
        groups = result.groups()
        
        # parsovani stavu
        pda.Q = self.matchItems(self.state_pattern, groups[0])

        # parsovani vstupni abecedy
        pda.Sigma = self.matchItems(self.symbol_pattern, groups[1])

        # parsovani zasobnikove abecedy
        pda.Gamma = self.matchItems(self.symbol_pattern, groups[2])
        
        # parsovani pravidel
        pda.R = self.matchRules(groups[3])

        # parsovani pocatecniho stavu
        pda.s = self.matchItem(self.state_pattern, groups[4])

        # parsovani pocatecniho symbolu
        pda.S = self.matchItem(self.symbol_pattern, groups[5])

        # parsovani zasobnikove abecedy
        pda.F = self.matchItems(self.state_pattern, groups[6])

        # vrati nacteny automat
        check(pda)
        return pda
