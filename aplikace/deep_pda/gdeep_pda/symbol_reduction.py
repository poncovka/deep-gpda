'''
Trida pro redukci nevstupnich symbolu GDP na tri.

@author: Vendula Poncova
'''

from .automaton import GDP, GDP_rule
from .error import check

# nastaveni paramentru pro debugging
DEBUG = True
DEBUG_CODE = "[SymbolReduction]"


class SymbolReduction:
    '''
    Umoznuje redukci nevstupnich symbolu v GDP automatech.
    '''

    def __init__(self):
        '''
        Constructor
        '''

#//////////////////////////////////////////////////////////////////// REDUKCE     
 
    def run(self, pda):
        '''
        Omezi pocet nevstupnich symbolu na tri.
        '''
        check("Redukce nevstupnich symbolu.", DEBUG_CODE, DEBUG, 0)

        # definovani funkce pro kodovani zasobnikovych symbolu
        coding = self.getCodingFunction(pda.Gamma)        
               
        # definice zredukovaneho automatu
        
        Sigma = pda.Sigma
        Gamma = pda.Sigma.union({"0","1","#"})
        s = "<start>"
        S = "#"
        F = {"<end>"}

        # konstrukce mnoziny Q
        Q = self.construct_Q(pda)
        
        # konstrukce mnoziny R
        R = self.construct_R(pda, coding)

        # vytvor vystupni automat
        output = GDP()
        output.set(Q, Sigma, Gamma, R, s, S, F)
        
        # pomocny vypis 
        check(output.serialize(), DEBUG_CODE, DEBUG, 2)
        
        output.validate()
        return output
    
#=================================================================== getCodingFunction()    
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

#=================================================================== code()    
    def code(self, zeros, ones = 0):
        return tuple("0") * zeros + tuple("1") * ones
    
#=================================================================== state()    
    def state(self, s, code, apostrof = 0):
        return "<" + s + "," + ''.join(code) + ">" + "'" * apostrof

#//////////////////////////////////////////////////////////////////// KONSTRUKCE Q        

    def construct_Q(self, pda):
        check("Konstrukce mnoziny stavu.", DEBUG_CODE, DEBUG, 1)
        
        Q = set()
        
        # konstrukce mnoziny stavu
        Q.add("<start>")
        Q.add("<end>")
        
        for q in pda.Q :
            for zeros in range(0, len(pda.Gamma) + 1) :
                for apostrof in (0, 1, 2) :
                    
                    Q.add(self.state(q, self.code(zeros),    apostrof))
                    Q.add(self.state(q, self.code(zeros, 1), apostrof))
                
        check("Stav mnoziny Q: \n" + str(Q), DEBUG_CODE, DEBUG, 3)
                
        return Q

#//////////////////////////////////////////////////////////////////// KONSTRUKCE R  
     
    def construct_R(self, pda, coding):
        
        R = set()
        
        # zkonstruuj mnoziny pravidel
        
        R_exp, Q_exp = self.construct_R_exp(pda, coding)
        
        R_find = self.construct_R_find(pda, coding)
        
        R_next = self.construct_R_next(pda, coding, Q_exp)
        
        R_move = self.construct_R_move(pda, coding)
        
        R_end = self.construct_R_end(pda, coding)
                   
        # sjednot je do jedne mnoziny
        
        R = R.union(R_exp)
        R = R.union(R_find)
        R = R.union(R_next)
        R = R.union(R_move)
        R = R.union(R_end)
        
        return R      

#=================================================================== construct_R_exp()    
    def construct_R_exp(self, pda, coding): 
        check("Konstrukce pravidel pro expanzi.", DEBUG_CODE, DEBUG, 1)
        
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
        
        check("Stav mnoziny R_exp: \n" + str(R_exp), DEBUG_CODE, DEBUG, 3)
        
        return R_exp, Q_exp

#=================================================================== construct_R_find()    
    def construct_R_find(self, pda, coding):   
        check("Konstrukce pravidel pro nacteni kodu.", DEBUG_CODE, DEBUG, 1)
        
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

        check("Stav mnoziny R_find: \n" + str(R_find), DEBUG_CODE, DEBUG, 3)
        
        return R_find

#=================================================================== construct_R_next()    
    def construct_R_next(self, pda, coding, Q_exp):
        check("Konstrukce pravidel pro presun na dalsi.", DEBUG_CODE, DEBUG, 1)
        
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
                
        check("Stav mnoziny R_next: \n" + str(R_next), DEBUG_CODE, DEBUG, 3)
        
        return R_next

#=================================================================== construct_R_move()    
    def construct_R_move(self, pda, coding):
        check("Konstrukce pravidel pro presun symbolu na konec.", DEBUG_CODE, DEBUG, 1)
        
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
                
                R_move.add(rule.get())
    
        for q in pda.Q :         
            
            # pravidlo (ix)                      
            rule.q = self.state( q, coding["#"], 1)
            rule.A = "#"
            rule.p = self.state( q, "", 0)
            rule.v = coding["#"] + tuple("#")
            
            R_move.add(rule.get())     
            
        check("Stav mnoziny R_move: \n" + str(R_move), DEBUG_CODE, DEBUG, 3)
        
        return R_move
    
#=================================================================== construct_R_end()    
    def construct_R_end(self, pda, coding):
        
        check("Konstrukce pravidel pro dokonceni.", DEBUG_CODE, DEBUG, 1)       
        
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
                
                R_end.add(rule.get())
                
        for q in pda.Q :         
            for X in pda.Gamma.difference(pda.Sigma) :
                
                # pravidlo (xi)                      
                rule.q = self.state( q, coding[X], 2)
                rule.A = "#"
                rule.p = self.state( q, "", 2)
                rule.v = coding[X] + tuple("#")
                
                R_end.add(rule.get())
                
        for q in pda.Q :         
            
            # pravidlo (xii)                              
            rule.q = self.state( q, coding["#"], 2)
            rule.A = "#"
            rule.p = "<end>"
            rule.v = ()
            
            R_end.add(rule.get())
        
        check("Stav mnoziny R_end: \n" + str(R_end), DEBUG_CODE, DEBUG, 3)
        
        return R_end

##################################################################### konec souboru        