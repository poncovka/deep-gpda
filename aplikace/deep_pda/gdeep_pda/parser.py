'''
Nacte z retezce zasobnikovy automat.
@author: Vendula Poncova
'''

import re
import string as pystring
from library import check, error, enum, error_more
from pda import GDP

class GDPParser:
    '''
    Parser pro nacteni GDP automatu z retezce.
    '''

##################################################################### init()

    def __init__(self):
        '''
        Nastavi vzory a regualrni vyrazy pro parsovani.
        '''

        # regularni vyraz pro vstupni symboly
        self.char_pattern = re.compile (r'''
        ('(?:''|[^'])*'|(?:(?:<[^>]*>|\[[^]]*\]|[^-{}, \t\n])+))
        ''', re.VERBOSE) 
 
        # regularni vyraz pro zasobnikove symboly
        self.symbol_pattern = re.compile (r'''
        ('(?:''|[^'])*'|(?:(?:<[^>]*>|\[[^]]*\]|[^-{}, \t\n])+))
        ''', re.VERBOSE) 
         
        # regularni vyraz pro stavy
        self.state_pattern = re.compile (r'''
        ('(?:''|[^'])*'|(?:(?:<[^>]*>|\[[^]]*\]|[^-{}, \t\n])+))
        ''', re.VERBOSE)
        
        # konstanty pro typ vzoru
        self.LIST = 0 
        self.GROUP = 1
        
        # vzor pro pravidlo
        self.rule_pattern = (self.LIST, (
                             self.state_pattern, 
                             self.symbol_pattern, 
                             "->", 
                             self.state_pattern, 
                             (self.GROUP, (self.symbol_pattern, "")))
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
        index = self.skipWhitespace(index,string)
   
        check("match: " + str(index))
        # aplikuje regularni vyraz na retezec
        result = pattern.match(string, index)
         
        # vrati False, nebo nalezene skupiny a index konce
        if result == None: 
            return None, index
        else :             
            check(result.group(0))
            return result.group(0), result.end()
          
#=================================================================== matchStr()
    
    def matchStr(self, pattern, index, string):
        '''
        Porovna retezec s prefixem retezce od aktualni pozice.
        '''
              
        # posun indexu za bile znaky
        old_index = index
        index = self.skipWhitespace(index,string)
        
        check("matchStr: " + str(index)+ ", " + pattern)
        
        # oddelovacem je whitespace
        if pattern == "" and old_index != index:
            return "", index
        
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
        check("matchGroup: " + str(index))
        
        group = list()
        pattern, separator = pattern
        
        item = True
        is_separator = False
        
        while item :
            check(is_separator)
            # ocekavam separator
            if is_separator :             
                
                # match retezce                
                item, index = self.matchItem(separator, index, string)
                
                # OK, pokracuj dalsi polozkou
                if item != None :
                    is_separator = False
                    check("separator ok")
                    
                # KONEC
                else:
                    check("Konec cyklu")
                    break
            
            # nacitani polozky    
            item, index = self.matchItem(pattern, index, string)
            
            if item != None :
                check("item ok")
                
                if not self.isConst(item, pattern):    
                    group.append(item)
                    
                is_separator = True
                
        # TODO separator nemuze zustat za
        #if is_separator == False and item == None:
        #    error_more("Lexikalni chyba v matchGroup.")
         
        check(group)   
        return group, index

#=================================================================== matchList()
                
    def matchList(self, patterns, index, string):
        '''
        Aplikuje seznam vzoru na aktualni pozici v retezci.
        '''
        check("matchItem: " + str(index))

        group = list()

        # prochazi seznam vzoru
        for pattern in patterns :
            
            # aplikuje vzor
            item, index = self.matchItem(pattern, index, string)
            
            # chyba
            if item == None :
                error_more("Lexikalni chyba v matchList.")
            
            # polozku uloz, pokud to neni konstanta
            if not self.isConst(item, pattern):    
                group.append(item)
        
        check(group)    
        return group, index

#=================================================================== matchItem()
        
    def matchItem(self, pattern, index, string):
        '''
        Aplikuje vzor na aktualni pozici v retezci.
        '''
        check("matchItem: " + str(index))
        
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
            
        check(item)
        
        # navrat    
        return item, index

##################################################################### run()
    
    def run(self, string):
        '''
        Nacteni PDA z retezce.
        '''
        check("Parsovani automatu.")
                
        # smazani komentaru
        string = re.sub("(//.*)", " ", string)

        # rozparsovanu vstupu
        group, index = self.matchItem(self.pda_pattern, 0, string)
        
        # zpracovani vysledku parsovani
        rules = list()
        
        for [q,A,p,v] in group[3] :
            
            # eliminace epsilon znaků
            w = list()
            
            for char in v:
                if char != "''" :
                    w.append(char)
            
            # sestaveni pravidla        
            rules.append((q,A,p,tuple(w)))    

        # vytvoreni noveho automatu
        pda = GDP()
        pda.set(group[0], group[1], group[2], rules, group[4], group[5], group[6])
        
        # vrati nacteny automat
        check(pda)
        return pda
    
##################################################################### konec souboru