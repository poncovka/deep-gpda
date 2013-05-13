'''
Testy pro parametry aplikace.

@author: Vendula Poncova
'''

import unittest
from .test_case import Test

from gdeep_pda import error

#####################################################################
class TestApplication(Test):


    def test(self):
        assert True

    def test_help(self):
        self.runApplication(["gdeep_pda", "--help"], 0, err = False, out = True)
        self.runApplication(["gdeep_pda", "-h"], 0, err = False, out = True)
        
    def test_err_params_01(self):
        self.runApplication(["gdeep_pda", "--chybny-param"], 
                            error.EPARAM().code, 
                            err = True, 
                            out = False)

    def test_err_params_02(self):
        self.runApplication(["gdeep_pda", "--help", "--reduce-states"], 
                            error.EPARAM().code, 
                            err = True, 
                            out = False)

    def test_err_params_03(self):
        self.runApplication(["gdeep_pda", "--max-steps=50"], 
                            error.EPARAM().code, 
                            err = True, 
                            out = False)
        
    def test_err_params_04(self):
        self.runApplication(["gdeep_pda", "--max-steps=-1", "--analyze-string=abcd"], 
                            error.EPARAM().code, 
                            err = True, 
                            out = False)
        
    def test_err_params_05(self):
        self.runApplication(["gdeep_pda", "--max-steps=abc", "--analyze-string=abcd"], 
                            error.EPARAM().code, 
                            err = True, 
                            out = False)

    def test_err_io_01(self):
        self.runApplication(["gdeep_pda", "--input="], 
                            error.EIO().code, 
                            err = True, 
                            out = False)
        
    def test_err_io_02(self):
        self.runApplication(["gdeep_pda", "--output=", "--input=input/test_ok_01"], 
                            error.EIO().code, 
                            err = True, 
                            out = False)
        
    def test_err_io_03(self):
        self.runApplication(["gdeep_pda", "--input=neexistujici_soubor"], 
                            error.EIO().code, 
                            err = True, 
                            out = False)
        
        
    def test_ok_io_01(self):
        
        self.print_input("({s},{a,b,c},{a,b,c,A,B,C},{s A -> s a b c},s,A,{s})")
        
        self.runApplication(["gdeep_pda"], 
                            0, 
                            err = False, 
                            out = True)

    
##################################################################### konec souboru