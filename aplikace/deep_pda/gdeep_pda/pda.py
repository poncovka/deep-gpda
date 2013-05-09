'''
Trida pro zobecneny hluboky zasobnikovy automat a jeho pravidla.

@author: Vendula Poncova
'''

from .error import check, EPDA

DEBUG = True
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
#===================================================================

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

#===================================================================

    def __str__(self):

        return ("Generalized Deep PDA: (\n"
                "" + str(self.Q) + "\n"
                "" + str(self.Sigma) + "\n"
                "" + str(self.Gamma) + "\n"
                "" + str(self.R) + "\n"
                "" + str(self.s) + "\n"
                "" + str(self.S) + "\n"
                "" + str(self.F) + "\n)")

#===================================================================

    def set(self, Q, Sigma, Gamma, R, s, S, F):
        
        self.Q = set(Q)
        self.Sigma = set(Sigma)
        self.Gamma = set(Gamma)
        self.R = set(R)
        self.s = s
        self.S = S
        self.F = set(F)

#===================================================================

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
            
#===================================================================

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
        Si.sort()

        Ga = list(self.Gamma)
        Ga.sort()

        # pravidla
        R = []
        for (q,A,p,v) in list(self.R) :
            
            rule = q + " " + A + " -> " + p
            if v : rule += " " + " ".join(v)
            
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

##################################################################### konec souboru       