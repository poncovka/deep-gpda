'''
Created on 12.5.2013

@author: wendy
'''

import unittest
import test.test_application
import test.test_parser

def suite():

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTest(loader.loadTestsFromModule(test.test_application))
    suite.addTest(loader.loadTestsFromModule(test.test_parser))
    
    return suite


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    
    try:
        runner = unittest.TextTestRunner()
        test_suite = suite()
        runner.run (test_suite)
    
    except SystemExit as inst:
        if inst.args[0] is True: # raised by sys.exit(True) when tests failed
            raise
