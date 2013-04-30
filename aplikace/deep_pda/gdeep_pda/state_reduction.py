'''
Created on 21.4.2013

@author: Vendula Poncova
'''

from pda import GDP, GDP_rule
from library import check

class StateReduction:
    '''
    Umoznuje redukci stavu ve GDP automatech.
    '''

    def __init__(self):
        '''
        Constructor
        '''

    def symbol(self, state, nonterm, label = None):
        
        if label == None :
            return "<" + state + "," + nonterm + ">"        
        elif label == "apostrof" :
            return "<" + state + "," + nonterm + ">" + "'"
        else:
            return "<" + state + "," + nonterm + "," + label + ">"
            
    def counter(self, number):
        return "<" + str(number) + ">"
 
    def getIndexFunction(self, Q):
        
        states = list(Q)   
        states.sort()  
        function = {}
        
        for i in range(0, len(states)) :
            function[ states[i] ] = i
            
        return function
    
    def getStateFunction(self, Q):
        
        states = list(Q)
        states.sort()
        states.append(states[0])
        
        function = {}
        
        for i in range(0, len(Q)) :
            function[ states[i] ] = states[i+1]
            
        return function
            
        
    def run(self, pda):
        '''
        Omezi pocet stavu na tri.
        '''
        check("Redukce stavu.")
               
        # zakladni definice
        Q = {"s_alpha", "s_beta", "s_gamma"}
        Sigma = pda.Sigma
        Gamma = set(pda.Sigma) # plus symboly definovane dale
        R = set()
        s = "s_alpha"
        S = "<start>"
        F = {"s_alpha"}
        
        # definice funkce pro nasledujici stavy
        next_state = self.getStateFunction(pda.Q)
        # definice funkce pro indexy stavu
        get_index = self.getIndexFunction(pda.Q)
        
        # konstrukce nevstupnich symbolu
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
                check(symbol)
                if symbol not in pda.Sigma:
                    rule.v += (self.symbol(q, symbol), )
                else :
                    rule.v += (symbol, )
                
            R_alpha.add(rule.get()) 
                
        
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
            
        # pravidla pro citac a koncovy symbol
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
        
        # konstrukce mnoziny pravidel
        
        R = R.union(R_alpha)
        R = R.union(R_beta)
        R = R.union(R_gamma)
        
        # vytvor vystupni automat
        output = GDP()
        output.set(Q, Sigma, Gamma, R, s, S, F)
         
        print(output.serialize())
        output.validate()
        
        return output
        
        