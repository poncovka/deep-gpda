'''
Nacte z retezce zasobnikovy automat.
@author: Vendula Poncova
'''

import re
import string as pystring
from .library import unquote, isSurrounded
from .error import check, EPDA
from .automaton import GDP

DEBUG = False
DEBUG_CODE = "[PARSER]"

class GDPParser:
    '''
    Parser pro nacteni GDP automatu z retezce.
    '''

##################################################################### init()

    def __init__(self):
        '''
        Nastavi vzory a regualrni vyrazy pro parsovani.
        '''
        
        # konstanty pro typ vzoru
        self.LIST = 0 
        self.GROUP = 1

        # regularni vyraz pro vstupni symboly
        self.char_pattern = re.compile (r'''
        (?:(\w+)|'((?:''|[^'])+)')
        ''', re.VERBOSE) 
        
        # regularni vyraz pro zasobnikove symboly
        self.symbol_pattern = re.compile (r'''
        (   \w+
          | ''
          | '(?:''|[^'])*'
          | \#
          | <(?:'[^']*'|[^>'])*>
        )
        ''', re.VERBOSE) 
                
        # regularni vyraz pro stavy
        self.state_pattern = re.compile (r'''
        (   \w+
          | <(?:'[^']*'|[^>'])*>
        )
        ''', re.VERBOSE) 
        
        # vzor pro pravidlo
        self.rule_pattern = (self.LIST, (
                             self.state_pattern, 
                             self.symbol_pattern, 
                             "->", 
                             self.state_pattern, 
                             (self.GROUP, (self.symbol_pattern, "\whitespace")))
                             )
        
        # vzor pro automat
        self.pda_pattern = (self.LIST, (
                            "(",
                            "{", (self.GROUP, (self.state_pattern,  ",")), "}", ",",
                            "{", (self.GROUP, (self.char_pattern,   ",")), "}", ",",
                            "{", (self.GROUP, (self.symbol_pattern, ",")), "}", ",",
                            "{", (self.GROUP, (self.rule_pattern,   ",")), "}", ",",
                            self.state_pattern,  ",",
                            self.symbol_pattern, ",",
                            "{", (self.GROUP, (self.state_pattern, ",")) , "}",
                            ")")
                            )
  

##################################################################### parsovani
  
    def skipWhitespace(self, index, string):
        '''
        Preskoci bile znaky a vrati upraveny index.
        '''
        while index < len(string) and string[index] in pystring.whitespace :
            index += 1
            
        return index    
                  
    def isConst(self, item, pattern):
        '''
        Vrati true, pokud je polozka konstanta.
        '''
        return isinstance(pattern, str)         

#=================================================================== match()
                  
    def match(self, pattern, index, string):
        '''
        Aplikuje na retezec regularni vyraz
        a vrati nalezeny retezec a index konce.
        '''
        # pomocny vypis
        check("match() na indexu " + str(index), DEBUG_CODE, DEBUG, 1)
            
        # vynechani stavu
        index = self.skipWhitespace(index,string)
   
        # aplikuje regularni vyraz na retezec
        result = pattern.match(string, index)
         
        # vrati False, nebo nalezene skupiny a index konce
        if result == None: 
            return None, index
        else :
            # pomocny vypis             
            check(result.group(0), DEBUG_CODE, DEBUG, 3)
            return result.group(0), result.end()
          
#=================================================================== matchStr()
    
    def matchStr(self, pattern, index, string):
        '''
        Porovna retezec s prefixem retezce od aktualni pozice.
        '''
              
        # posun indexu za bile znaky
        old_index = index
        index = self.skipWhitespace(index,string)
        
        # pomocny vypis
        check("matchStr() na indexu " + str(index) + ", vzor " + pattern, DEBUG_CODE, DEBUG, 1)
        
        # oddelovacem je whitespace
        if pattern == "\whitespace" and old_index != index:
            return pattern, index
        
        # oddelovacem je znak
        if string.startswith(pattern, index) :
            index += len(pattern)
            return pattern, index
    
        else:
            return None, index
            
#=================================================================== matchGroup()
        
    def matchGroup(self, pattern, index, string):
        '''
        Aplikuje pravidla na polozky oddelene separatorem.
        Vrati seznam nalezenych polozek.
        '''
        # pomocny vypis
        check("matchGroup() na indexu " + str(index), DEBUG_CODE, DEBUG, 1)
        
        group = list()
        pattern, separator = pattern
        
        item = True
        is_separator = False
        
        while item :
            
            # pomocny vypis
            check(is_separator, DEBUG_CODE, DEBUG, 3)
            
            # ocekavam separator
            if is_separator :             
                
                # match retezce                
                item, index = self.matchItem(separator, index, string)
                
                # OK, pokracuj dalsi polozkou
                if item != None :
                    is_separator = False
                    # pomocny vypis
                    check("Separator je nalezen.", DEBUG_CODE, DEBUG, 3)
                    
                # KONEC
                else:
                    # pomocny vypis
                    check("Konec cyklu pro parsovani skupiny.", DEBUG_CODE, DEBUG, 3)
                    break
            
            # nacitani polozky    
            item, index = self.matchItem(pattern, index, string)
            
            if item != None :
                # pomocny vypis
                check("Polozka je nalezena.", DEBUG_CODE, DEBUG, 3)
                
                if not self.isConst(item, pattern):    
                    group.append(item)
                    
                is_separator = True
                
        # TODO separator nemuze zustat za
        #if is_separator == False and item == None:
        #    error_more("Lexikalni chyba v matchGroup.")
        
        # pomocny vypis 
        check(group, DEBUG_CODE, DEBUG, 3)   
        
        return group, index

#=================================================================== matchList()
                
    def matchList(self, patterns, index, string):
        '''
        Aplikuje seznam vzoru na aktualni pozici v retezci.
        '''
        # pomocny vypis
        check("matchList() na indexu " + str(index), DEBUG_CODE, DEBUG, 1)

        group = list()

        # prochazi seznam vzoru
        for pattern in patterns :
            
            # aplikuje vzor
            item, index = self.matchItem(pattern, index, string)
            
            # chyba
            if item == None :
                raise EPDA("Chyba v syntaxi automatu.")
            
            # polozku uloz, pokud to neni konstanta
            if not self.isConst(item, pattern):    
                group.append(item)
        
        # pomocny vypis
        check(group, DEBUG_CODE, DEBUG, 3)
            
        return group, index

#=================================================================== matchItem()
        
    def matchItem(self, pattern, index, string):
        '''
        Aplikuje vzor na aktualni pozici v retezci.
        '''
        # pomocny vypis
        check("matchItem() na indexu " + str(index), DEBUG_CODE, DEBUG, 1)
        
        item = None
        
        # vzorem jeretezec
        if isinstance(pattern, str):
            
            item, index = self.matchStr(pattern, index, string)
        
        # vzorem je sekvence pravidel
        elif isinstance(pattern,tuple) :
            
            # urci typ sekvence
            type_pattern, next_pattern = pattern
            
            # sekvence pravidel
            if type_pattern == self.LIST :
                item, index = self.matchList(next_pattern, index, string)
            
            # skupina pravidel oddelena separatorem
            elif type_pattern == self.GROUP:
                item, index = self.matchGroup(next_pattern, index, string)
        
        # vzorem je regularni vyraz           
        elif isinstance(pattern, re._pattern_type) :
            
            item, index = self.match(pattern, index, string)
            
        # pomocny vypis
        check(item, DEBUG_CODE, DEBUG, 3)
        
        # navrat    
        return item, index


##################################################################### parseString()

    def parseString(self, string):
        
        pattern = (self.GROUP, (self.char_pattern, "\whitespace"))
        
        group, index = self.matchItem(pattern, 0, string)
        group = unquote(group)
        
        if index != len(string) :
            return None
        else:
            return group

##################################################################### checkQuote()

    def checkQuote(self, symbol, group):
        
        if isSurrounded(symbol, "'", "'" ) :
            if symbol not in group and unquote(symbol) not in group :
                #print(symbol, symbol not in group[1], unquote(symbol) not in group[1])
                raise EPDA("Nevstupni symboly nesmi byt v uvozovkach.")

##################################################################### run()

    
    def run(self, string):
        '''
        Nacteni PDA z retezce.
        '''
        # pomocny vypis
        check("Parsovani automatu.", DEBUG_CODE, DEBUG, 0)
        
        try :        
            # smazani komentaru
            string = re.sub("(//.*)", " ", string)
        
            # rozparsovanu vstupu
            group, index = self.matchItem(self.pda_pattern, 0, string)
                        
            #kontrola uvozovek v nevstupnich symbolech
            for symbol in group[2] :
                self.checkQuote(symbol, group[1])
             
            for [q,symbol,p,v] in group[3] :
                self.checkQuote(symbol, group[1])
                
                for symbol in v :
                    if symbol != "''" :
                        self.checkQuote(symbol, group[1])
                    
            self.checkQuote(group[5], group[1])
                
            # odstraneni uvozovek
            group = unquote(group)
            
            # zpracovani vysledku parsovani
            rules = list()
            
            for [q,A,p,v] in group[3] :
                
                # eliminace epsilon znaků
                w = list()
                
                for char in v:
                    if char != "" :
                        w.append(char)
                
                # sestaveni pravidla        
                rules.append((q,A,p,tuple(w)))
                    
        except Exception:            
            raise EPDA("Chyba v syntaxi automatu.")

        # vytvoreni noveho automatu
        pda = GDP()
        pda.set(group[0], group[1], group[2], rules, group[4], group[5], group[6])
        
        # pomocny vypis
        check(pda, DEBUG_CODE, DEBUG, 2)
        
        # vrati nacteny automat
        return pda
    
##################################################################### konec souboru