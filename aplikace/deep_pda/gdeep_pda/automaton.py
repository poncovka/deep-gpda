'''
Trida pro zobecneny hluboky zasobnikovy automat a jeho pravidla.

@author: Vendula Poncova
'''

from .error import check, EPDA
from .library import tableprint, quote, unquote


DEBUG = False
DEBUG_CODE = "[PDA]"

##################################################################### GDP_rule

class GDP_rule:
    '''
    Trida reprezentujici pravidlo typu:
      q A -> p v, 
    kde p,q jsou stavy, A je nevstupni
    symbol a v je retezec.
    '''
    
    def __init__(self):
        
        self.q = None
        self.A = None
        self.p = None
        self.v = None
        
    def get(self):
        return (self.q, self.A, self.p, self.v)

##################################################################### GDP

class GDP:
    '''
    Trida reprezentuje zobecneny hluboky zasobnikovy automat,
    GDP je zkratka pro Generalized Deep PDA.
    '''
#=================================================================== init()

    def __init__(self):
        '''
        Constructor
        Inicializace promennych.
        '''
        
        self.Q = set()
        self.Sigma = set()
        self.Gamma = set()
        self.R = set()
        self.s = None
        self.S = None
        self.F = set()

#=================================================================== str()

    def __str__(self):

        return ("Generalized Deep PDA: (\n"
                "" + str(self.Q) + "\n"
                "" + str(self.Sigma) + "\n"
                "" + str(self.Gamma) + "\n"
                "" + str(self.R) + "\n"
                "" + str(self.s) + "\n"
                "" + str(self.S) + "\n"
                "" + str(self.F) + "\n)")

#=================================================================== set()

    def set(self, Q, Sigma, Gamma, R, s, S, F):
        
        self.Q = set(Q)
        self.Sigma = set(Sigma)
        self.Gamma = set(Gamma)
        self.R = set(R)
        self.s = s
        self.S = S
        self.F = set(F)

#=================================================================== validate()

    def validate(self):
        
        check("Kontrola spravnosti GDP automatu.", DEBUG_CODE, DEBUG, level = 0)
        
        # abecedy a stavy

        if len(self.Q) == 0 :
            raise EPDA("Prazdna mnozina stavu.")
        if len(self.Sigma) == 0 or len(self.Gamma) == 0 :
            raise EPDA("Prazdna abeceda.")
        if not self.Sigma.issubset(self.Gamma):
            raise EPDA("Vstupni abeceda neni podmnozinou zasobnikove.")
        if self.Q.intersection(self.Gamma) != set() :
            raise EPDA("Stavy a symboly nejsou disjunktni.")
        if self.s not in self.Q:
            raise EPDA("Pocatecni stav neni v mnozine stavu.")
        if self.S not in self.Gamma.difference(self.Sigma) :
            raise EPDA("Pocatecni symbol neni v mnozine nevstupnich symbolu.")
        if not self.F.issubset(self.Q) :
            raise EPDA("Mnozina koncovych stavu neni podmnozinou stavu.")
        if '' in self.Gamma :
            raise EPDA("Prazdny retezec nemuze byt soucasti abecedy.")
            
        # pravidla
        for (q, A, p ,v) in self.R :
            check((q,A,p,v), DEBUG_CODE, DEBUG, level = 3)
            
            if q not in self.Q or p not in self.Q:
                raise EPDA("V pravidle se vyskytuje nedefinovany stav.")
            if A not in self.Gamma.difference(self.Sigma):
                raise EPDA("Na leve strane pravidla neni nevstupni symbol.")
               
            for symbol in v :
                if symbol not in self.Gamma:
                    raise EPDA("Na prave strane pravidla je nedefinovany symbol.")     
            
#=================================================================== serializace
               

    def serializeRule(self, rule):
        
        (q,A,p,v) = rule
        
        str_rule = q + " " + A + " -> " + p
        if v :
            v = quote(list(v),self.Sigma)
            str_rule += " " + " ".join(v)
        
        return str_rule
    
    def serializeDerivation(self, backtracking, string):
        
        derivation_table = list()
        head = ["","", "state", "input", "pushdown","", "rule"]
        
        for (state, index, pushdown, step, rule) in backtracking :
            
            pushdown = quote(list(pushdown), self.Sigma)
            
            derivation   = "=>" if derivation_table else ""
            str_state    = state + ", "
            str_input    = "'" + "".join(string[index:]) + "'" + ", "
            str_pushdown = " ".join(reversed(pushdown))
            str_rule     = "[ " + self.serializeRule(rule) + " ] " if rule else ""
            
            derivation_table.append([derivation, "(", str_state, str_input, str_pushdown, ")", str_rule])            

        derivation_table.insert(0, head)
        
        return tableprint(derivation_table, head)

    def serialize(self):
        '''
        Formatovany vypis automatu.
        '''        
        check("Serializace PDA.", DEBUG_CODE, DEBUG, level = 0)

        # stavy
        Q = list(self.Q)
        Q.sort()

        F = list(self.F)
        F.sort()

        # abecedy
        Si = list(self.Sigma)
        Si = quote(Si,self.Sigma)
        Si.sort()

        Ga = list(self.Gamma)
        Ga = quote(Ga, self.Sigma)
        Ga.sort()

        # pravidla
        R = []
        for r in list(self.R) :
            
            rule = self.serializeRule(r)
            R.append(rule)
            
        R.sort()    
        
        # vytvoreni a vraceni retezce
        string = ("(\n"
                  "{"   + ", ".join(Q)  +     "},\n"
                  "{"   + ", ".join(Si) +     "},\n"
                  "{"   + ", ".join(Ga) +     "},\n"
                  "{\n"   + ",\n".join(R) + "\n},\n"
                  "" + str(self.s) + ",\n"
                  "" + str(self.S) + ",\n"
                  "{"   + ", ".join(F)  +     "}\n" 
                  ")\n"
                  )

        return string
        
#=================================================================== analyze string
        
    def getTop(self,x):
        return x[-1]

    def expand(self, string, index):
        
        self.pushdown.pop(index)
        self.pushdown[index:index] = reversed(string)

    def getConfiguration(self):
        return(self.state, self.index, tuple(self.pushdown))
        
    def saveDerivation(self, backtracking, step = 0, rule = None):
        
        backtracking.append((self.state, self.index, tuple(self.pushdown), step, rule))
        
    def loadDerivation(self, backtracking):
        
        self.state, self.index, pushdown, step, rule = backtracking.pop()
        self.pushdown = list(pushdown)
        
        return step + 1

    def analyze(self, string, max_step = 500):
        
        check("Analyza retezce.", DEBUG_CODE, DEBUG, level = 0)
        result = True
        
        # sestaveni struktury pro prochazeni pravidly
        rules = dict()
        
        for (q,A,p,v) in self.R :
            
            if (q,A) not in rules :
                rules[(q,A)] = list()
                
            rules[(q,A)].append((p, v))
            
        check(rules, DEBUG_CODE, DEBUG, 3)
        
        # inicializace automatu
        self.state = self.s
        self.index = 0
        self.pushdown = list()
        self.pushdown.append(self.S)

        # backbacktracking a historie
        backtracking = list()
        step = 0
        
        self.saveDerivation(backtracking, step)
                        
        
        while self.pushdown or self.index < len(string) or self.state not in self.F:
            
            check("STATE " + str(self.getConfiguration()), DEBUG_CODE, DEBUG, 3)
            
            topsymbol   = self.getTop(self.pushdown) if self.pushdown else None
            char        = string[self.index]         if self.index < len(string) else None 
            
            if char and topsymbol and char == topsymbol :
                    
                check("POP " + str(char), DEBUG_CODE, DEBUG, 3)
                
                self.index += 1
                self.pushdown.pop()
                self.saveDerivation(backtracking, step)
                
            else:
                expanded = False
                
                for i in range(len(self.pushdown) - 1, -1, -1):
                    
                    symbol = self.pushdown[i]
                    
                    if (self.state, symbol) in rules and len(rules[(self.state, symbol)]) > step:
                        
                        next_state, next_string = rules[(self.state, symbol)][step]
                        
                        check("EXPAND" + self.state +" "+ symbol +" -> "+ next_state + " " + " ".join(next_string), DEBUG_CODE, DEBUG, 3)
                        
                        self.state = next_state
                        self.expand(next_string, i)
                        
                        self.saveDerivation(backtracking, step, (self.state, symbol, next_state, next_string ))
                        expanded = True
                        step = 0
                        break
                        
                if not expanded or len(backtracking) > max_step:
                    
                    if len(backtracking) > max_step:
                        check("MAX STEP", DEBUG_CODE, DEBUG, 3)
                    
                    if backtracking :
                        step = self.loadDerivation(backtracking)
                        check("BACKTRACKING " + str(step), DEBUG_CODE, DEBUG, 3)
                    else:
                        result = False
                        break        
        
        check("END " + str(self.getConfiguration()) + ", steps + " + str(len(backtracking)), DEBUG_CODE, DEBUG, 3)
        
        if result :
            derivation = self.serializeDerivation(backtracking, string)
        else:
            derivation = None
        
        return result, derivation

##################################################################### konec souboru       