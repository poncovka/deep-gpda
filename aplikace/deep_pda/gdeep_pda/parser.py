'''
Nacte z retezce zasobnikovy automat.
@author: Vendula Poncova
'''

import re

from library import check, error
from pda import GDP

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
        \s*\{((?:'[^']*'|[^}])*)\}\s*,
        \s*\{((?:'[^']*'|[^}])*)\}\s*,
        \s*\{((?:'[^']*'|[^}])*)\}\s*,
        \s*\{((?:'[^']*'|[^}])*)\}\s*,
        \s*((?:'[^']*'|<[^>]*>|[^,])*)\s*,
        \s*((?:'[^']*'|<[^>]*>|[^,])*)\s*,
        \s*\{((?:'[^']*'|[^}])*)\}\s*
        \)\s*$
        ''', re.VERBOSE)     

        self.symbol_pattern = re.compile (r'''
        ^\s*
        ('(?:''|[^'])*'|(?:(?:<[^>]*>|\[[^]]*\]|[^-{}, \t\n])+))
        \s*
        ''', re.VERBOSE) 
        
        self.state_pattern = re.compile (r'''
        ^\s*
        ((?:<[^>]*>|\[[^]]*\]|[^-{}, \t\n])+)
        \s*
        ''', re.VERBOSE)
        
        self.arrow_pattern = re.compile (r'''
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
        
        # vrati False, nebo nalezene skupiny a index konce
        if result == None: return False
        else :             return result.groups(), result.end()
    
    def matchGroups(self, string):
        
        # parsovani automatu
        result = self.match(self.pda_pattern, string)
        
        # chyba ve vstupnim retezci
        if not result: error("EPDA")
        
        # skupiny
        return result[0]
    
    def matchGroup(self, patterns, string):
        '''
        Nacte z retezce polozky oddelene carkou
        '''
        
        group = list()
        items = list()
        
        start = 0
        end = len(string)
        comma = False
        
        # dokud neprojde cely retezec
        while start < end :
            
            # v retezci nasleduje oddelovac carka
            if comma and string[start] == ',' :
                
                # nastav promenne
                start += 1
                comma = False
                
                # uloz polozky do skupiny
                group.append(list(items))
                # zaloz novou skupinu polozek
                items = list()               
            
            # vyhledej skupinu polozek
            for pattern in patterns:
                #check(string[start:])
                # aplikuje regularni vyraz na retezec
                result = self.match(pattern, string[start:])
                
                if result:                      
                    # posune se ukazatel na retezec
                    start += result[1]
                    # nova polozka se ulozi
                    items.append(result[0][0])
                    # nastavi se indikator oddelovace
                    comma = True
                    # vyskoc z cyklu
                    break
            
            # zadna polozka, chyba 
            if not comma :
                error("EPDA")
 
        # uloz polozky do skupiny
        group.append(list(items))
                    
        # vrati prvky skupiny
        return group
 
    def matchSet(self, pattern, string):
        
        group = self.matchGroup((pattern,), string)
        result = set()

        for items in group :
            for item in items :
                result.add(item)
            
        return result
    
    def matchItem(self, pattern, string):
        
        items = self.matchSet(pattern, string)
        return items.pop()
    
    def matchRules(self, string):
        '''
        Nacte pravidla z retezce
        '''
        
        patterns_left = (self.state_pattern, 
                         self.symbol_pattern,
                         self.arrow_pattern, 
                         self.state_pattern)
                 
        group = self.matchGroup( patterns_left + (self.symbol_pattern,), string)
        
        rules = set()
        
        check(group)
        
        for items in group :
            
            rule_right = list()
            rule_left = list()
            
            index = 0
            
            for item in items:
               
                if index < len(patterns_left):
                   
                    result = self.match(patterns_left[index], item)
                   
                    if not result: 
                        error("EPDA")
                    else:
                        rule_left.append(item)
                        
                else:
                    
                    result = self.match(self.symbol_pattern, item)
                   
                    if result: 
                            
                        if item != "''" :
                            rule_right.append(item)
                        break
                    
                    else : 
                        error("EPDA") 
                        
                index += 1
                
            #rules.add((rule_left.append(rule_right)))
            rule = (rule_left[0], rule_left[1], rule_left[3], tuple(rule_right))
            rules.add(rule)
            
            check(rules)
            
        return rules
                        
    def run(self, string):
        '''
        Nacteni PDA z retezce.
        '''
        check("Parsovani automatu.")
        
        # smazani komentaru
        string = re.sub("(//.*)", " ", string)

        # vytvoreni noveho automatu
        pda = GDP()
        
        # parsovani automatu
        groups = self.matchGroups(string)
                
        # parsovani stavu
        check("Parsovani stavu.")
        pda.Q = self.matchSet(self.state_pattern, groups[0])

        # parsovani vstupni abecedy
        check("Parsovani Sigma.")
        pda.Sigma = self.matchSet(self.symbol_pattern, groups[1])

        # parsovani zasobnikove abecedy
        check("Parsovani Gamma.")
        pda.Gamma = self.matchSet(self.symbol_pattern, groups[2])
        
        # parsovani pravidel
        check("Parsovani pravidel.")
        pda.R = self.matchRules(groups[3])

        # parsovani pocatecniho stavu
        check("Parsovani poc. stavu.")
        pda.s = self.matchItem(self.state_pattern, groups[4])

        # parsovani pocatecniho symbolu
        check("Parsovani poc. symbolu.")
        pda.S = self.matchItem(self.symbol_pattern, groups[5])

        # parsovani koncovych stavu
        check("Parsovani koncovych stavu.")
        pda.F = self.matchSet(self.state_pattern, groups[6])

        # vrati nacteny automat
        check(pda)
        return pda
