'''
Test suite - spusteni vsech testu.

@author: Vendula Poncova
'''

import unittest
from test import *

def suite(tests):

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
        
    if not tests :
        suite.addTest(loader.discover(".", "test_*.py"))
    else:
        suite.addTest(loader.loadTestsFromNames(tests))
        
    return suite


def main(argv):
    
    tests = argv[1:] 
    
    try:
        runner = unittest.TextTestRunner()
        test_suite = suite(tests)
        runner.run (test_suite)
    
    except SystemExit as inst:
        if inst.args[0] is True: # raised by sys.exit(True) when tests failed
            raise
