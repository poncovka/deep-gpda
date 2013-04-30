'''
Created on 21.4.2013

@author: Vendula Poncova
'''

from pda import GDP, GDP_rule
from library import check

class SymbolReduction:
    '''
    Umoznuje redukci nevstupnich symbolu v GDP automatech.
    '''


    def __init__(self):
        '''
        Constructor
        '''
    
    def getCodingFunction(self, symbols):
        '''
        Definice kodovaci funkce.
        Kazdemu symbolu priradi jedinecnou
        kominaci nul a jednicek.
        '''
        
        function = {}
        
        # definice symbolu
        index = 1
        for symbol in symbols :
            
            function[symbol] = self.code(index, 1)
            index += 1
        
        # definice specialniho symbolu konce zasobniku
        function["#"] = tuple("1")  
        
        return function
    
    def code(self, zeros, ones = 0):
        return tuple("0") * zeros + tuple("1") * ones
    
    def state(self, s, code, apostrof = 0):
        return "<" + s + "," + ''.join(code) + ">" + "'" * apostrof
        
    def run(self, pda):
        '''
        Omezi pocet nevstupnich symbolu na tri.
        '''
        check("Redukce nevstupnich symbolu.")
               
        # zakladni definice
        Q = set()
        Sigma = pda.Sigma
        Gamma = pda.Sigma.union({"0","1","#"})
        R = set()
        s = "<start>"
        S = "#"
        F = {"<end>"}
        
        # definovani funkce pro kodovani zasobnikovych symbolu
        coding = self.getCodingFunction(pda.Gamma)        
        
        # konstrukce mnoziny stavu
        Q.add("<start>")
        Q.add("<end>")
        
        for q in pda.Q :
            for zeros in range(0, len(pda.Gamma) + 1) :
                for apostrof in (0, 1, 2) :
                    
                    Q.add(self.state(q, self.code(zeros),    apostrof))
                    Q.add(self.state(q, self.code(zeros, 1), apostrof))
                
        # konstrukce mnoziny pravidel PRO EXPANZI
        Q_exp = set()
        R_exp = set()
        rule = GDP_rule()
        
        # pravidlo (i)
        rule.q = "<start>"
        rule.A = "#"
        rule.p = self.state(pda.s, "")
        rule.v = coding[pda.S] + coding["#"] + tuple("#")
        
        R_exp.add(rule.get())
        
        # pro kazde pravidlo vstupniho automatu
        for (q,A,p,v) in pda.R :
            
            # pravidlo (ii)
            rule.q = self.state(q, coding[A])
            rule.A = "#"
            rule.p = self.state(p, "", 1)
                  
            rule.v = tuple()
            
            for symbol in v :
                rule.v += coding[symbol]
                 
            rule.v += tuple("#")
            
            R_exp.add(rule.get())
            Q_exp.add(rule.q)
        
        # konstrukce mnoziny pravidel PRO NACTENI KODU
        R_find = set()
        rule = GDP_rule()
        
        for q in pda.Q :
            for zeros in range(0, len(pda.Gamma)) :
                for apostrof in range(0, 2) :
                    
                    # pravidla (iii), (iv), (v)
                    rule.q = self.state(q, self.code(zeros),     apostrof)
                    rule.A = "0"
                    rule.p = self.state(q, self.code(zeros + 1), apostrof)
                    rule.v = ()
                    
                    R_find.add(rule.get())
                    
                    rule.q = self.state(q, self.code(zeros),        apostrof)
                    rule.A = "1"
                    rule.p = self.state(q, self.code(zeros + 1, 1), apostrof)
                    rule.v = ()
                    
                    R_find.add(rule.get())

        # konstrukce mnoziny pravidel PRO PRESUN NA DALSI
        R_next = set()
        rule = GDP_rule()

        for X in pda.Gamma :
            for q in pda.Q :
                if self.state (q, coding[X] ) not in Q_exp :                   
                    
                    # pravidlo (vi)            
                    rule.q = self.state( q, coding[X] )
                    rule.A = "#"
                    rule.p = self.state( q, "")
                    rule.v = coding[X] + tuple("#")
                    
                    R_next.add(rule.get())
        
        for q in pda.Q :
            
            # pravidlo (vii)            
            rule.q = self.state( q, coding["#"], 0)
            rule.A = "#"
            rule.p = self.state( q,   "",        2)
            rule.v = coding["#"] + tuple("#")
            
            R_next.add(rule.get())
                
        
        # konstrukce mnoziny pravidel PRO PRESUNUTI SYMBOLU NA KONEC
        R_move = set()
        rule = GDP_rule()

        for q in pda.Q :         
            for X in pda.Gamma :
                
                # pravidlo (viii)                      
                rule.q = self.state( q, coding[X], 1)
                rule.A = "#"
                rule.p = self.state( q, "", 1)
                rule.v = coding[X] + tuple("#")
                
                R_next.add(rule.get())
    
        for q in pda.Q :         
            
            # pravidlo (ix)                      
            rule.q = self.state( q, coding["#"], 1)
            rule.A = "#"
            rule.p = self.state( q, "", 0)
            rule.v = coding["#"] + tuple("#")
            
            R_next.add(rule.get())            
        
        # konstrukce mnoziny pravidel PRO DOKONCENI
        R_end = set()
        rule = GDP_rule()

        for q in pda.Q :         
            for X in pda.Sigma :
                
                # pravidlo (x)                      
                rule.q = self.state( q, coding[X], 2)
                rule.A = "#"
                rule.p = self.state( q, "", 2)
                rule.v = ( X, "#" )
                
                R_next.add(rule.get())
                
        for q in pda.Q :         
            for X in pda.Gamma.difference(pda.Sigma) :
                
                # pravidlo (xi)                      
                rule.q = self.state( q, coding[X], 2)
                rule.A = "#"
                rule.p = self.state( q, "", 2)
                rule.v = coding[X] + tuple("#")
                
                R_next.add(rule.get())
                
        for q in pda.Q :         
            
            # pravidlo (xii)                              
            rule.q = self.state( q, coding["#"], 2)
            rule.A = "#"
            rule.p = "<end>"
            rule.v = ()
            
            R_next.add(rule.get())
          
           
        # vytvor mnozinu pravidel
        R = R.union(R_exp)
        R = R.union(R_find)
        R = R.union(R_next)
        R = R.union(R_move)
        R = R.union(R_end)
        
        # vytvor vystupni automat
        output = GDP()
        output.set(Q, Sigma, Gamma, R, s, S, F)
         
        #print(output.serialize())
        output.validate()
        return output
        