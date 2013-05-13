'''
Created on 12.5.2013

@author: wendy
'''
import unittest
from .test_case import Test

from gdeep_pda import library

#####################################################################
class TestLibrary(Test):
    
    path = "test/input/"

    def test(self):
        assert True

    def test_unquote_ok(self):
        self.assertEqual(library.unquote("'ahoj'"), "ahoj")
        self.assertEqual(library.unquote("'ahoj svete'"), "ahoj svete")
        self.assertEqual(library.unquote("'a'"), "a")

    def test_surrounded_ok(self):
        self.assertEqual(library.isSurrounded("'ahoj'", "'", "'"), True)
        self.assertEqual(library.isSurrounded("'ahoj svete'", "'", "'"), True)
        self.assertEqual(library.isSurrounded("'a'", "'", "'"), True)
        
#####################################################################

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    
    runner = unittest.TextTestRunner()
    test_suite = TestLibrary().suite()
    runner.run (test_suite)
    
##################################################################### konec souboru