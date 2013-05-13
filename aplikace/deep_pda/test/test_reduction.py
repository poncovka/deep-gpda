'''
Created on 12.5.2013

@author: wendy
'''
import unittest
from .test_case import Test

#####################################################################
class TestReduction(Test):
    
    path = "test/input/"

    def test(self):
        assert True

    def runReduction_ok(self, type, file, file2):
        
        out = self.runApplication(["gdeep_reduce", 
                                   "--input=" + self.path + file, 
                                   "--reduce-" + type ], 
                                  0, 
                                  err = False, 
                                  out = True)
        
        f = open(self.path + file2, mode='r', encoding='utf8')
        out2 = f.read()
        
        self.assertEqual(out, out2, "Srovnani automatu.")
        
    def test_ok_reduce_symbols_01(self):
        self.runReduction_ok("symbols", "test_ok_08", "test_ok_symbols_01")

    def test_ok_reduce_symbols_02(self):        
        self.runReduction_ok("symbols", "test_ok_01", "test_ok_symbols_02")

    def test_ok_reduce_states_01(self):
        self.runReduction_ok("states", "test_ok_08", "test_ok_states_01")

    def test_ok_reduce_states_02(self):        
        self.runReduction_ok("states", "test_ok_01", "test_ok_states_02")
            
#####################################################################

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    
    runner = unittest.TextTestRunner()
    test_suite = TestReduction().suite()
    runner.run (test_suite)
    
##################################################################### konec souboru