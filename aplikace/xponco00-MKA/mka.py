#!usr/bin/python3

#MKA:xponco00

# IPP - 2. projekt : MKA, duben 2012
# Vendula Poncova, xponco00@stud.fit.vutbr.cz

import sys
import re
import codecs

debug = False
error_code = {"EPARAM": 1, "EREAD": 2, "EWRITE": 3, 
              "EKA": 60,   "EDKA": 61, "EDSKA" : 62}

################################################## Pomocne skripty

def check(string):
    '''Funkce pro kontrolni vypisy.'''
    if debug:
        sys.stderr.write("> " + str(string) + "\n")

def error(msg, code):
    '''Vypise chybovou hlasku a skonci.'''
    sys.stderr.write("ERR: " + msg + "\n", )
    sys.exit(error_code[code])

def quote(symbol):
    '''Vrati symbol obaleny apostrofy.'''
    return "'"+symbol+"'"

def unquote(symbol):
    '''Odstrani obalujici apostrofy.'''
    if   len(symbol) == 4 : symbol = "''"
    elif len(symbol) == 3 : symbol = symbol[1]
    elif len(symbol) == 2 : symbol = ""

    return symbol

def is_unique(a,b,c):
    '''Je prave jeden, nebo zadny, pravda?'''
    return  not((a and b) or (b and c) or (a and c))

def printHelp():
    help = '''
    MKA: Minimalizace konecneho automatu
    Vendula Poncova (xponco00)

    mka [-h] [--input=filename] [--output=filename] [-f] [-m] [-i]
        [--analyze-string="string"] [--wsfa]


    -h, --help                   Vypise napovedu.
    --input=filename             Nacte vstup ze souboru.
    --output=filename            Vypise vystup do souboru.
    -f, --find-non-finishing     Najde neukoncujici stav.
    -m, --minimize               Provede minimalizaci.
    -i, --case-insensitive       Nebude bran ohled na velikost pismen.
    --analyze-string="string"    Vrati 1, pokud je string retezec jazyka
                                 prijimaneho konecnym automatem, jinak 0.
    --wsfa                       Provede transformaci DKA na DSKA.
    \n'''
    sys.stdout.write(help)

def processParams():
    check("Zpracovani parametru:")   

    options = {"--input": "input", "--output": "output", "--analyze-string": "analyze_string"}

    bool_options = { "--help": "help",                             "-h": "help",
                     "--find-non-finishing": "find_non_finishing", "-f": "find_non_finishing", 
                     "--minimize": "minimize",                     "-m": "minimize",
                     "--case-insensitive": "case_insensitive",     "-i": "case_insensitive",                   
                     "--wsfa": "wsfa"
                   }
    args = {} 

    # zpracovani parametru
    for arg in sys.argv[1:]:
        (opt, sep, value) = arg.partition("=")

        if arg in bool_options and bool_options[arg] not in args:
            args[bool_options[arg]] = True

        elif opt in options and options[opt] not in args:
            args[options[opt]] = value

        else: error("Spatne zadane parametry.", "EPARAM")

    # kontrola dodatecnych podminek
    if not is_unique("find_non_finishing" in args, "minimize" in args, "analyze_string" in args) :
        error("Spatne zadane parametry.", "EPARAM")

    if ("help" in args) and len(args) != 1:
        error("Spatne zadane parametry.", "EPARAM")

    check(args)
    return args


def readInput (args):
    check("Nacteni vstupu:")
    try:
        if "input" in args :
            file = open(args["input"], mode='r', encoding='utf-8')
            input = file.read()
            file.close()
        else:
            input = sys.stdin.read()

    except IOError:
        error("Nepodarilo se nacteni ze souboru.", "EREAD")

    check(input)
    return input

def writeOutput(output, args):
    check("Zápis výstupu:")
    check(output)
    try:
        if "output" in args :
            file = open(args["output"], mode='w', encoding='utf-8')
            file.write(output)
            file.close()
        else:
            file = sys.stdout.write(output)

    except IOError:
        error("Nepodaril se zapis do souboru..", "EWRITE")


################################################## Trida Konecny automat

class FSM:
    ''' Trida popisujici konecny automat.'''

    Q = set()
    E = set()
    R = {}
    s = None
    F = set()

    def __init__(self):
        check("Novy konecny automat.")

    def getRule(self, state, symbol):
        '''Vrati klic pro slovnik R.'''
        return state + " " + quote(symbol);

    def addRule(self, state, symbol, nextstate):
        '''Prida pravidlo do slovniku R.'''
        self.R[self.getRule(state, symbol)] = nextstate

    def splitRule(self, rule):
        '''Rozdeli klic klic slovniku R na stav a symbol.'''
        (state, separator, symbol) = rule.partition(" ")
        return (state,symbol)

    def makeTransition(self, state, symbol):
        '''Vrati stav po prechodu.'''
        return self.R[self.getRule(state,symbol)]

    def analyzeString(self, string):
        '''Analyza, zda je retezec retezcem jazyka prijimaneho KA.'''
        # pocatecni stav
        state = self.s

        # provadej prechody
        for char in string:
            if char not in self.E: 
                return 0
            elif self.getRule(state,char) not in self.R: 
                return 0
            else :
                state = self.makeTransition(state, char)

        # skoncili jsme v koncovem stavu?
        if state in self.F : return 1
        else:                return 0

    def prettyprint(self):
        '''Formatovany vypis automatu.'''
        check("Pretty print:")

        # stavy
        Q = list(self.Q)
        Q.sort()

        # koncove stav
        F = list(self.F)
        F.sort()

        # abeceda
        E = []
        for item in self.E:
            E.append("'"+ item +"'")

        E.sort()

        # pravidla
        rules = []
        for item in self.R:
            (state, symbol) = self.splitRule(item)
            rules.append((state, unquote(symbol), self.R[item]))

        rules.sort()

        R = []
        for item in rules:
            R.append(item[0] + " " + quote(item[1]) + " -> " + item[2])
        
        # vytvoreni retezce
        stringQ = "{"   + ", ".join(Q)  +   "},\n"
        stringE = "{"   + ", ".join(E)  +   "},\n"
        stringR = "{\n" + ",\n".join(R) + "\n},\n"
        strings =  self.s               +    ",\n"
        stringF = "{"   + ", ".join(F)  +    "}\n"

        string = "(\n"+ stringQ + stringE + stringR + strings + stringF + ")"

        check(string)
        return string

    def checkDKA(self):
        '''Kontrola, zda je automat DKA.'''

        if len(self.E) == 0 : 
            error("Prazdna abeceda.", "EDKA")
        if self.Q.intersection(self.E) != set() : 
            error("Nejsou disjunktni znaky a stavy.", "EDKA")
        if self.s not in self.Q : 
            error("Pocatecni symbol neni definovan v Q.", "EDKA")
        if not self.F.issubset(self.Q) : 
            error("F neni podmnozinou Q.", "EDKA")

        for rule in self.R :
            (state, symbol) = self.splitRule(rule)

            if state not in self.Q :
                error("Nedefinovany stav.", "EDKA")

            if symbol == "''": 
                error("Obsahuje epsilon prechody.", "EDKA")
            elif unquote(symbol) not in self.E : 
                error("Nedefinovany symbol.", "EDKA")

            if self.R[rule] not in self.Q :
                error("Nedefinovany stav.", "EDKA")

        check("Spravne definovany KA.")

    def checkDSKA(self):
        '''Kontrola, zda je automat DSKA.'''
        self.checkDKA()

        # nema nedostupne stavy
        if len(self.findNonAvailable()) != 0 :
            error("Ma nedostupne stavy.", "EDSKA")

        # ma max. jeden neukoncujici stav
        if len(self.findNonFinishing()) > 1 :
            error("Ma vice neukoncujicich stavu.", "EDSKA")

        # uplny automat
        for state in self.Q :
            for symbol in self.E:
                if self.getRule(state,symbol) not in self.R:
                    error("Neuplny automat.", "EDSKA")

        check("Spravne definovany DSKA.")

    def findNonAvailable(self):
        '''Vrati mnozinu nedpstupnych stavu.'''
        check("Hledani nedostupnych stavu")

        availableSet = set()
        newAvailableSet = set()

        availableSet.add(self.s)
        change = True

        while change :
            for available in availableSet :
                for rule in self.R :
                    (state, symbol) = self.splitRule(rule)
                    if available == state:
                        newAvailableSet.add(self.R[rule])

            if newAvailableSet.difference(availableSet) == set(): 
                change = False
            else:
                availableSet.update(newAvailableSet)
                newAvailableSet.clear()

        check(self.Q.difference(availableSet))
        return self.Q.difference(availableSet)        

    def findNonFinishing(self):
        '''Vrati mnozinu neukoncujicich stavu.'''
        check("Hledani neukoncujicich stavu")

        finishingSet = set(self.F)
        newFinishingSet = set()
        change = True

        while change :
            for finishing in finishingSet :
                for rule in self.R :
                    if self.R[rule] == finishing:
                        (state, symbol) = self.splitRule(rule)
                        newFinishingSet.add(state)

            if newFinishingSet.difference(finishingSet) == set(): 
                change = False
            else:
                finishingSet.update(newFinishingSet)
                newFinishingSet.clear()

        check(self.Q.difference(finishingSet))
        return self.Q.difference(finishingSet)

    def transformToDSKA(self):
        '''Prevede DKA na ekvivalentni DSKA.'''

        nonfinState = "qFalse"
        trap = False

        # smazani zbytecnych stavu
        delete_states = self.findNonFinishing().union(self.findNonAvailable())
        self.Q = self.Q.difference(delete_states)
        self.F = self.F.difference(delete_states)

        # promazani hran
        for rule in list(self.R):
            (state, symbol) = self.splitRule(rule)
            nextstate = self.R[rule]
            if state in delete_states or nextstate in delete_states:
                del self.R[rule]

        # doplneni do uplneho automatu
        for state in list(self.Q):
            for symbol in self.E:
                rule = self.getRule(state,symbol)
                if rule not in self.R :
                    trap = True
                    self.R[rule] = nonfinState

        # doplneni pasti
        if trap:
            self.Q.add(nonfinState)
            for symbol in self.E:
                rule = self.getRule(nonfinState,symbol)
                self.R[rule] = nonfinState 

        if self.s not in self.Q:
            self.s = nonfinState
        
################################################## Trida Parser

class FSM_parser:
    ''' Trida pro parsovani fsm.'''

    fsmPattern = None
    statePattern = None
    symbolPattern = None

    def __init__(self):
        check("Inicializace vzoru.")

        self.fsmPattern = re.compile (r'''
        ^\s*\(
        \s*\{((?:'}'|'{'|[^}{])*)\}\s*,
        \s*\{((?:'}'|'{'|[^}{])*)\}\s*,
        \s*\{((?:'}'|'{'|[^}{])*)\}\s*,
        \s*((?:','|[^,])*)\s*,\s*
        \s*\{((?:'}'|'{'|[^}{])*)\}\s*
        \)\s*$
        ''', re.VERBOSE)
        self.statePattern = re.compile ('^\s*([^\W_0-9](?:\w*[^\W_])?)\s*')
        self.symbolPattern = re.compile ('^\s*(\'\'\'\'|\'\'|\'[^\']\'|[^-(){}\'>,.|# \t\n])\s*')

    def matchFsm(self, string):
        '''Kontrola struktury KA a rozdeleni na komponenty.'''
        found = re.match(self.fsmPattern, string)

        if found == None : error("Spatny format konecneho automatu.", "EKA")
        return found.groups()

    def matchItem(self, string, start, pattern, quiet = False):
        '''Parsovani prvku komponenty podle vzoru.'''
        item = re.match(pattern, string[start:])

        if item == None : 
            if not quiet: error("Spatny format prvku.", "EKA")
            else:         item = "''"   
        else: 
            start = start + item.end()
            item = item.groups()[0]

        return (item, start)
  
    def matchGroup(self, string, pattern):
        '''Parsovani komponenty.'''

        output = set()
        comma = False

        start = 0
        end = len(string)

        while start < end :
            if comma: 
                if string[start] == ',' : start = start + 1
                else : error("Spatny format komponenty.", "EKA")
                comma = False
            else:
                (item, start) = self.matchItem(string, start, pattern)
                comma = True
                output.add(item)

        return output

    def matchRule(self, string):
        '''Parsovani komponenty pravidel.'''

        output = {}
        comma = False

        start = 0
        end = len(string)

        while start < end :
            if comma: 
                if string[start] == ',' : start = start + 1
                else : error("Spatny format komponenty.", "EKA")
                comma = False
            else:
                # stav
                (state, start) = self.matchItem(string, start, self.statePattern)

                # symbol
                (symbol, start) = self.matchItem(string, start, self.symbolPattern, quiet = True)

                # sipka
                if start + 2 < end and string[start:start+2] == "->" : start = start + 2
                else : error("Spatny format pravidla.", "EKA")

                # dalsi stav
                (nextstate, start) = self.matchItem(string, start, self.statePattern)

                # carka
                comma = True

                # pridej nove pravidlo
                if len(symbol) == 1 : symbol = "'"+symbol+"'"
                output[state + " " + symbol] = nextstate

        return output
        

    def run(self, input):
        '''Nacteni KA z retezce.'''

        # smazani komentaru
        input = re.sub("(#.*)", " ", input)
        check("Vstup:\n" + input + "\n");

        check("Parsovani.")
        fsm = FSM()

        # parsovani fsm
        group = self.matchFsm(input)

        # mnozina stavu
        fsm.Q = self.matchGroup(group[0], self.statePattern)

        # abeceda
        E = self.matchGroup(group[1], self.symbolPattern)
        for symbol in E :
            if unquote(symbol) == "" : error("Epsilon je znak abecedy.", "EKA")
            fsm.E.add(unquote(symbol))

        # pravidla
        fsm.R = self.matchRule(group[2])
        
        # pocatecni stav
        (fsm.s, cnt) = self.matchItem(group[3], 0, self.statePattern)

        if cnt != len(group[3]) : error("Spatny format pocatecniho stavu.", "EKA")

        # koncove stavy
        fsm.F = self.matchGroup(group[4], self.statePattern)

        return fsm

################################################## Trida Minimize

class FSM_minimize:
    '''Trida pro minimalizaci konecneho automatu.'''

    mini_states = {}

    def __init__(self):
        check("Novy minimalizator")

    def clean(self):
        '''Inicializace tridni promenne.'''
        self.mini_states = {}

    def getName(self, states):
        '''Vygeneruje identifikator mnoziny sloucenych stavu.'''
        states = list(states)
        states.sort()
        return "_".join(states)

    def getStates(self, name):
        '''Vrati mnozinu sloucenych stavu.'''
        if name in self.mini_states :  
            return self.mini_states[name]
        else: 
            return set()        

    def addStateSet(self, stateSet):
        '''Prida novy slouceny stav'''
        if stateSet != set() :
            name = self.getName(stateSet)
            self.mini_states[name] = stateSet

    def getStateSet(self, state) :
        '''Vrati identifikator mnoziny sloucenych stavu.'''
        for name in self.mini_states:
            if state in self.mini_states[name]:
                return name

        return None

    def splitStateSet(self, name, groupA, groupB):
        '''Rozstepeni stavu na dva nove.'''

        # vymazani puvodniho stavu
        del self.mini_states[name]

        # pridani dvou novych stavu
        self.addStateSet(groupA)
        self.addStateSet(groupB)

    def run(self, fsm):
        '''Spusteni minimalizace'''
        check("Minimalizace:")

        # inicializace
        self.addStateSet(fsm.F)
        self.addStateSet(fsm.Q.difference(fsm.F))

        change = True

        # iteruj dokud zmena
        while change:
            change = False

            # pro stavy minimalizovateho automatu
            Q = set(self.mini_states)
            for stateSet in Q:

                # pro vsechny symboly abecedy
                for symbol in fsm.E:

                    stateA = ""
                    groupA = set()
                    groupB = set()

                    # prochazej sloucene stavy
                    for state in self.getStates(stateSet):
                        
                        # ziskej stav po prechodu a jmeno mnoziny stavu
                        nextstate = fsm.makeTransition(state,symbol)
                        nextstateSet = self.getStateSet(nextstate)

                        # rozdel stavy do skupin
                        if stateA == "" or stateA == nextstateSet: 
                            stateA = nextstateSet
                            groupA.add(state)
                        else:
                            groupB.add(state)

                    # rozstepeni
                    if groupB != set():
                        self.splitStateSet(stateSet, groupA, groupB)
                        change = True

        # novy automat:
        check(self.mini_states)

        minifsm = FSM()
        minifsm.Q = set(self.mini_states)
        minifsm.E = fsm.E

        # pravidla
        for state in fsm.Q :
            for symbol in fsm.E:
                nextstate = fsm.makeTransition(state, symbol)

                stateSet = self.getStateSet(state)
                nextstateSet = self.getStateSet(nextstate)
                
                minifsm.addRule(stateSet, symbol, nextstateSet)
            
        # pocatecti stav
        minifsm.s = self.getStateSet(fsm.s)

        # koncove stavy
        for stateSet in self.mini_states :
            if self.mini_states[stateSet].intersection(fsm.F) != set() :
                minifsm.F.add(stateSet)

        self.clean()
        return minifsm

################################################## Main skript

if __name__ == '__main__':
    check("Spusteni skriptu.")

    # zpracovani parametru
    args = processParams()

    # tisk napovedy
    if "help" in args :
        printHelp()
        exit(0)
    
    # nacteni vstupu
    input = readInput(args)

    # ignorovat velikost pismen?
    if "case_insensitive" in args :
        input = input.lower()

    # nacteni automatu
    fsm = FSM_parser().run(input)
    
    # kontrola automatu
    if "wsfa" in args:
        fsm.checkDKA()
        fsm.transformToDSKA()

    fsm.checkDSKA()

    # operace nad fsm
    if "find_non_finishing" in args:
        output = fsm.findNonFinishing()
        if output is not set() : output = output.pop()
        else :                   output = ""

    elif "analyze_string" in args:
        output = str(fsm.analyzeString(args["analyze_string"]))

    elif "minimize" in args:
        minifsm = FSM_minimize().run(fsm)
        output = minifsm.prettyprint()
    else:
        output = fsm.prettyprint()

    # tisk vystupu
    writeOutput(output, args)


################################################## Konec souboru))
