'''
Created on 12.5.2013

@author: wendy
'''
import unittest
from .test_case import Test

from gdeep_pda import error

#####################################################################
class TestParser(Test):
    
    path = "test/input/"

    def test(self):
        assert True

    def runParser_ok(self, file):
        
        out = self.runApplication(["gdeep_pda", "--input=" + self.path + file], 
                                  0, 
                                  err = False, 
                                  out = True)
        
        self.checkOutput(out)
        return out

    def runParser_err(self, file):
        
        out = self.runApplication(["gdeep_pda", "--input=" + self.path + file], 
                                  error.EPDA().code, 
                                  err = True, 
                                  out = False)
        return out
    
    def checkOutput(self, input):
        
        self.tearDown()
        self.setUp()
        
        self.print_input(input)
        
        output = self.runApplication(["gdeep_pda"], 
                                  0, 
                                  err = False, 
                                  out = True)
        
        self.assertEqual(input, output, "Vstup programu neni stejny jako vystup." )

            
    def test_ok_pda_01(self):
        self.runParser_ok("test_ok_01")

    def test_ok_pda_02(self):
        self.runParser_ok("test_ok_02")
    
    def test_ok_pda_03(self):
        self.runParser_ok("test_ok_03")
    
    def test_ok_pda_04(self):
        self.runParser_ok("test_ok_04")

    def test_ok_pda_05(self):
        self.runParser_ok("test_ok_05")

    def test_ok_pda_06(self):
        self.runParser_ok("test_ok_06")
        
    def test_ok_pda_07(self):
        self.runParser_ok("test_ok_07")
        
    def test_ok_pda_08(self):
        self.runParser_ok("test_ok_08")

    def test_ok_pda_09(self):
        self.runParser_ok("test_ok_09")
            
    def test_err_pda_01(self):
        self.runParser_err("test_err_01")

    def test_err_pda_02(self):
        self.runParser_err("test_err_02")
        
    def test_err_pda_03(self):
        self.runParser_err("test_err_03")

    def test_err_pda_04(self):
        self.runParser_err("test_err_04")

    def test_err_pda_05(self):
        self.runParser_err("test_err_05")

    def test_err_pda_06(self):
        self.runParser_err("test_err_06")

    def test_err_pda_07(self):
        self.runParser_err("test_err_07")

    def test_err_pda_08(self):
        self.runParser_err("test_err_08")

    def test_err_pda_09(self):
        self.runParser_err("test_err_09")
        
    def test_err_pda_10(self):
        self.runParser_err("test_err_10")
        
    def test_err_pda_11(self):
        self.runParser_err("test_err_11")

#####################################################################

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    
    runner = unittest.TextTestRunner()
    test_suite = TestParser().suite()
    runner.run (test_suite)
    
##################################################################### konec souboru