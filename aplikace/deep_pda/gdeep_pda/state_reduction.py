'''
Trida pro redukci stavu GDP na tri.

@author: Vendula Poncova
'''

from .automaton import GDP, GDP_rule
from .error import check

# nastaveni parametru pro debugging
DEBUG = True
DEBUG_CODE = "[StateReduction]"

class StateReduction:
    '''
    Umoznuje redukci stavu ve GDP automatech.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        
#//////////////////////////////////////////////////////////////////// REDUKCE            
        
    def run(self, pda):
        '''
        Omezi pocet stavu na tri.
        '''
        check("Redukce stavu.", DEBUG_CODE, DEBUG, 0)

        # definice funkce pro nasledujici stavy
        next_state = self.getStateFunction(pda.Q)
        
        # definice funkce pro indexy stavu
        get_index = self.getIndexFunction(pda.Q)
                       
        # definice zredukovaneho automatu
        Q = {"s_alpha", "s_beta", "s_gamma"}
        Sigma = pda.Sigma
        s = "s_alpha"
        S = "<start>"
        F = {"s_alpha"}
        
        # konstrukce mnoziny zasobnikovych symbolu
        Gamma = self.construct_Gamma(pda)
        
        # konstrukce pravidel
        R = self.construct_R(pda, next_state, get_index)  
        
        # vytvor vystupni automat
        output = GDP()
        output.set(Q, Sigma, Gamma, R, s, S, F)
         
        # pomocny vypis
        check(output.serialize(), DEBUG_CODE, DEBUG, 2)
        
        # kontrola spravnosti automatu
        output.validate()
        
        return output
    
#=================================================================== symbol()
    def symbol(self, state, nonterm, label = None):
        
        if label == None :
            return "<" + state + "," + nonterm + ">"        
        elif label == "apostrof" :
            return "<" + state + "," + nonterm + ">" + "'"
        else:
            return "<" + state + "," + nonterm + "," + label + ">"
            
#=================================================================== counter()
    def counter(self, number):
        return "<" + str(number) + ">"

#=================================================================== getIndexFunction() 
    def getIndexFunction(self, Q):
        
        states = list(Q)   
        states.sort()  
        function = {}
        
        for i in range(0, len(states)) :
            function[ states[i] ] = i
            
        return function

#=================================================================== getStateFunction()    
    def getStateFunction(self, Q):
        
        states = list(Q)
        states.sort()
        states.append(states[0])
        
        function = {}
        
        for i in range(0, len(Q)) :
            function[ states[i] ] = states[i+1]
            
        return function

#//////////////////////////////////////////////////////////////////// KONSTRUKCE GAMMA

    def construct_Gamma(self, pda):
        
        check("Konstrukce nevstupnich symbolu.", DEBUG_CODE, DEBUG, 1)
        
        # konstrukce nevstupnich symbolu
        Gamma = set(pda.Sigma)
        Gamma.add("<start>")
        
        for j in range(1, len(pda.Q) + 1) :
            Gamma.add(self.counter(j))
        
        for q in pda.Q :
            for X in pda.Gamma.difference(pda.Sigma):
                Gamma.add(self.symbol(q, X))
                Gamma.add(self.symbol(q, X, "apostrof"))    
            
        for q in pda.Q:
            Gamma.add(self.symbol(q, "#"))
            Gamma.add(self.symbol(q, "#", "set"))
            Gamma.add(self.symbol(q, "#", "exp"))
        
        check("Stav mnoziny Gamma: \n" + str(Gamma), DEBUG_CODE, DEBUG, 3)
        
        return Gamma

#//////////////////////////////////////////////////////////////////// KONSTRUKCE R  
        
    def construct_R(self, pda, next_state, get_index):
        
        R = set()
        
        # zkonstruuj mnoziny pravidel
        
        R_alpha_expand = self.construct_R_alpha_expand(pda, next_state, get_index)
        
        R_alpha_others = self.construct_R_alpha_others(pda, next_state, get_index)

        R_beta = self.construct_R_beta(pda, next_state, get_index)
        
        R_gamma = self.construct_R_gamma(pda, next_state, get_index)
   
        # sjednot je do jedne
        
        R = R.union(R_alpha_expand)
        R = R.union(R_alpha_others)
        R = R.union(R_beta)
        R = R.union(R_gamma)
        
        return R   

#=================================================================== construct_R_alpha_expand() 
    def construct_R_alpha_expand(self, pda, next_state, get_index):  
        
        check("Konstrukce pravidel pro expanzi.", DEBUG_CODE, DEBUG, 1)

        ## pravidla pro EXPANZI
        R_alpha = set()
        rule = GDP_rule()
        
        # pravidlo (i)
        rule.q = "s_alpha"
        rule.A = "<start>"
        rule.p = "s_alpha"
        rule.v = (self.symbol(pda.s, pda.S), self.symbol(pda.s, "#"))
        
        R_alpha.add(rule.get())
        
        # pravidla (ii) a (iii)
        for (q,A,p,v) in pda.R :
            
            rule.q = "s_alpha"
            rule.A = self.symbol(q, A)
            
            # nedojde ke zmene stavu
            if p == q :
                rule.p = "s_alpha"
                rule.v = tuple()
                
            # dojde ke zmene stavu, generuje se citac
            else:
                rule.p = "s_beta"
                rule.v = ( self.counter( abs(get_index[q] - get_index[p]) ) ,)
            
            # uprava prave strany pravidla
            for symbol in v :
                check(symbol, DEBUG_CODE, DEBUG, 3)
                if symbol not in pda.Sigma:
                    rule.v += (self.symbol(q, symbol), )
                else :
                    rule.v += (symbol, )
                
            R_alpha.add(rule.get()) 
        
        check("Stav mnoziny R_alpha: \n" + str(R_alpha), DEBUG_CODE, DEBUG, 3)    
        
        return R_alpha 

#=================================================================== construct_R_alpha_others()    
    def construct_R_alpha_others(self, pda, next_state, get_index):
        
        check("Konstrukce pravidel pro citac a koncovy symbol.", DEBUG_CODE, DEBUG, 1)
        
        # pravidla pro citac a koncovy symbol
        R_alpha = set()
        rule = GDP_rule()
        
        # pravidlo (vi) 
        for j in range(2, len(pda.Q) + 1):
            
            rule.q = "s_alpha"
            rule.A = self.counter(j)
            rule.p = "s_gamma"
            rule.v = (self.counter(j - 1) ,)
            
            R_alpha.add(rule.get())
        
        # pravidlo (vii)
        rule.q = "s_alpha"
        rule.A = self.counter(1)
        rule.p = "s_alpha"
        rule.v = ()
        
        R_alpha.add(rule.get())    
        
        # pravidlo (viii)
        for q in pda.Q :
            rule.q = "s_alpha"
            rule.A = self.symbol(q, "#", "set")
            rule.p = "s_gamma"
            rule.v = (self.symbol(q, "#", "exp") ,)
            
            R_alpha.add(rule.get())
  
        # pravidlo (ix)
        for q in pda.F :
            rule.q = "s_alpha"
            rule.A = self.symbol(q, "#")
            rule.p = "s_alpha"
            rule.v = ()
            
            R_alpha.add(rule.get())            
        
        check("Stav mnoziny R_alpha: \n" + str(R_alpha), DEBUG_CODE, DEBUG, 3)
        
        return R_alpha  

#=================================================================== construct_R_beta()
    def construct_R_beta(self, pda, next_state, get_index):
        
        check("Konstrukce pravidel pro znackovani.", DEBUG_CODE, DEBUG, 1)
        
        # pravidla pro ZNACKOVANI
        R_beta = set()
        rule = GDP_rule()
        
        # pravidlo (iv)
        
        for q in pda.Q :
            for X in pda.Gamma.difference(pda.Sigma):
                
                rule.q = "s_beta"
                rule.A = self.symbol(q, X)
                rule.p = "s_beta"
                rule.v = (self.symbol(next_state[q], X, "apostrof"), )
                
                R_beta.add(rule.get())
        
        # pravidlo (v)        
        for q in pda.Q :
            
            rule.q = "s_beta"
            rule.A = self.symbol(q, "#")
            rule.p = "s_alpha"
            rule.v = (self.symbol(next_state[q], "#", "set"))
        
        check("Stav mnoziny R_beta: \n" + str(R_beta), DEBUG_CODE, DEBUG, 3)
        
        return R_beta
 
#=================================================================== construct_R_gamma()
    def construct_R_gamma(self, pda, next_state, get_index):
        check("Konstrukce pravidel pro odznackovani.", DEBUG_CODE, DEBUG, 1)
        
        # pravidla pro ODZNACKOVANI
        R_gamma = set()
        rule = GDP_rule()        
        
        # pravidlo (x)
        for q in pda.Q :
            for X in pda.Gamma.difference(pda.Sigma):
                
                rule.q = "s_gamma"
                rule.A = self.symbol(q, X, "apostrof")
                rule.p = "s_gamma"
                rule.v = (self.symbol(q, X), )
                
                R_gamma.add(rule.get())
        
        for q in pda.Q :
            
            # pravidlo (xi)
            rule.q = "s_gamma"
            rule.A = self.symbol(q, "#", "set")
            rule.p = "s_beta"
            rule.v = (self.symbol(q, "#"), )
            
            R_gamma.add(rule.get())
            
            # pravidlo (xii)
            rule.q = "s_gamma"
            rule.A = self.symbol(q, "#", "exp")
            rule.p = "s_alpha"
            rule.v = (self.symbol(q, "#"), )
            
            R_gamma.add(rule.get())
        
        check("Stav mnoziny R_gamma: \n" + str(R_gamma), DEBUG_CODE, DEBUG, 3)
        
        return R_gamma 
        
##################################################################### konec souboru        