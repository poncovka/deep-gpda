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
        return out

    def runParser_err(self, file):
        
        out = self.runApplication(["gdeep_pda", "--input=" + self.path + file], 
                                  error.EPDA().code, 
                                  err = True, 
                                  out = False)
        return out
            
    def test_ok_pda_01(self):
        out = self.runParser_ok("test_ok_01")

    def test_ok_pda_02(self):
        out = self.runParser_ok("test_ok_02")
    
    def test_ok_pda_03(self):
        out = self.runParser_ok("test_ok_03")
    
    def test_ok_pda_04(self):
        out = self.runParser_ok("test_ok_04")

    def test_ok_pda_05(self):
        out = self.runParser_ok("test_ok_05")

    def test_ok_pda_06(self):
        out = self.runParser_ok("test_ok_06")
            
    def test_err_pda_01(self):
        out = self.runParser_err("test_err_01")

    def test_err_pda_02(self):
        out = self.runParser_err("test_err_02")
        
    def test_err_pda_03(self):
        out = self.runParser_err("test_err_03")

    def test_err_pda_04(self):
        out = self.runParser_err("test_err_04")

    def test_err_pda_05(self):
        out = self.runParser_err("test_err_05")

    def test_err_pda_06(self):
        out = self.runParser_err("test_err_06")

    def test_err_pda_07(self):
        out = self.runParser_err("test_err_07")

#####################################################################

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    
    runner = unittest.TextTestRunner()
    test_suite = TestParser().suite()
    runner.run (test_suite)
    
##################################################################### konec souboru