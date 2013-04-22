'''
Created on 21.4.2013

@author: Vendula Poncova
'''

from library import check, error_more

class GDP:
    '''
    Trida reprezentuje zobecneny hluboky zasobnikovy automat,
    GDP je zkratka pro Generalized Deep PDA.
    '''

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

    def __str__(self):

        return ("Generalized Deep PDA: (\n"
                "" + str(self.Q) + "\n"
                "" + str(self.Sigma) + "\n"
                "" + str(self.Gamma) + "\n"
                "" + str(self.R) + "\n"
                "" + str(self.s) + "\n"
                "" + str(self.S) + "\n"
                "" + str(self.F) + "\n)")

    def validate(self):
        
        check("Kontrola spravnosti GDP automatu")
        
        # abecedy a stavy

        if len(self.Q) == 0 :
            error_more("Prazdna mnozina stavu.")
        if len(self.Sigma) == 0 or len(self.Gamma) == 0 :
            error_more("Prazdna abeceda.")
        if not self.Sigma.issubset(self.Gamma):
            error_more("Vstupni abeceda neni podmnozinou zasobnikove.")
        if self.Q.intersection(self.Gamma) != set() :
            error_more("Stavy a symboly nejsou disjunktni.")
        if self.s not in self.Q:
            error_more("Pocatecni stav neni v mnozine stavu.")
        if self.S not in self.Gamma.difference(self.Sigma) :
            error_more("Pocatecni symbol neni v mnozine nevstupnich symbolu.")
        if not self.F.issubset(self.Q) :
            error_more("Mnozina koncovych stavu neni podmnozinou stavu.")
        if '' in self.Gamma :
            error_more("Prazdny retezec nemuze byt soucasti abecedy.")
            
        # pravidla
        for (q, A, p ,v) in self.R :
            
            if q not in self.Q or p not in self.Q:
                error_more("V pravidle se vyskytuje nedefinovany stav.")
            if A not in self.Gamma.difference(self.Sigma):
                error_more("Na leve strane pravidla neni nevstupni symbol.")
               
            for symbol in v :
                if symbol not in self.Gamma:
                    error_more("Na prave strane pravidla je nedefinovany symbol.")     
            

    def serialize(self):
        '''
        Formatovany vypis automatu.
        '''        
        check("Serializace PDA:")

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
            
        R.sort    
        
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

        