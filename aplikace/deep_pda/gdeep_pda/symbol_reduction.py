'''
Created on 21.4.2013

@author: Vendula Poncova
'''

from pda import GDP
from library import check

class SymbolReduction:
    '''
    Umoznuje redukci nevstupnich symbolu v GDP automatech.
    '''


    def __init__(self):
        '''
        Constructor
        '''
    
    def defCodingFunction(self, symbols):
        '''
        Definice kodovaci funkce.
        Kazdemu symbolu pripradi jedinecnou
        kominaci nul a jednicek.
        '''
        
        function = {}
        
        # definice symbolu
        index = 1
        for symbol in symbols :
            
            function[symbol] = "0" * index + "1"
            index += 1
        
        # definice specialniho symbolu konce zasobniku
        function["#"] = "1"  
        
        return function
    
    def state(self, s, code, apostrof = 0):
        return "<" + s + "," + code + ">" + "'" * apostrof
    
#     def rule(self, (a,b,c), A, (d,e,f), *v ):
#         return ( self.state(a,b,c),
#                  A, 
#                  self.state(d,e,f),
#                  (symbol for symbol in v) ) 
        
    def run(self, pda):
        '''
        Omezi pocet nevstupnich symbolu na tri.
        '''
        check("Redukce nevstupnich symbolu.")
        
        # vysledny automat
        output = GDP()
        
        # zakladni definice
        output.Sigma = pda.Sigma
        output.Gamma = pda.Sigma.union({"0","1","#"})
        output.s = "<start>"
        output.S = "#"
        output.F = {"<end>"}
        
        # definovani funkce pro kodovani zasobnikovych symbolu
        coding = self.defCodingFunction(pda.Gamma)        
        
        # konstrukce mnoziny stavu
        output.Q.add("<start>")
        output.Q.add("<end>")
        
        for q in pda.Q :
            for i in range(0, len(pda.Gamma)) :
                for j in range(0, 2) :
                    output.Q.add(self.state(q, "0" * i, j))
                    output.Q.add(self.state(q, "0" * i + "1", j))
                
        # konstrukce mnoziny pravidel PRO EXPANZI
        Q_exp = set()
        R_exp = set()
        
        # pridej pravidlo pro pocatecni symbol a stav
        R_exp.add(("<start>",
                   "#",
                   self.state(pda.s, ""),
                   (coding[pda.S], coding["#"], "#" )
                   ))
        
        # pro kazde pravidlo vstupniho automatu
        for (q,A,p,v) in pda.R :
            
            # pridej do pomocne mnoziny vychozi stav pravidla
            Q_exp.add(self.state(q,coding[A]))
            
            # vytvor ekvivalentni pravidlo
            R_exp.add((self.state(q, coding[A]), 
                      "#", 
                      self.state(p, "", 1),   
                      tuple( coding[symbol] for symbol in v ) + ("#",)
                      ))
        
        # konstrukce mnoziny pravidel PRO NACTENI KODU
        R_find = set()
        
        for q in pda.Q :
            for i in range(0, len(pda.Gamma)) :
                for j in range(0, 2) :
                    R_find.add((self.state(q, "0" * i, j), 
                                "0",
                                self.state(q, "0" * (i+1), j), 
                                ()
                                ))                                
                    R_find.add((self.state(q, "0" * i, j), 
                                "1",
                                self.state(q, "0" * (i+1) + "1", j), 
                                ()
                                ))

        # konstrukce mnoziny pravidel PRO PRESUN NA DALSI
        R_next = set()
        
        for q in pda.Q :
            R_next.add((self.state(q,coding["#"],0), 
                        "#",
                        self.state(q, "", 2), 
                        (coding["#"], "#")
                        ))
        
        # konstrukce mnoziny pravidel PRO PRESUNUTI SYMBOLU NA KONEC
        R_move = set()
        
        # konstrukce mnoziny pravidel PRO DOKONCENI
        R_end = set()
           
        # vytvor mnozinu pravidel
        output.R = output.R.union(R_exp)
        output.R = output.R.union(R_find)
        output.R = output.R.union(R_next)
        output.R = output.R.union(R_move)
        output.R = output.R.union(R_end)
        
        #str(output.serialize())
        #out_pda.validate()
        return output
        