'''
Created on 12.5.2013

@author: wendy
'''
import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import unittest
from io import StringIO

from gdeep_pda import application

class Test(unittest.TestCase):


    def setUp(self):
        # presmerovani vystupu
        self.saved_stdout, sys.stdout = sys.stdout, StringIO()
        self.saved_stderr, sys.stderr = sys.stderr, StringIO()

    def tearDown(self):
        # presmerovani vystupu
        sys.stdout.close()
        sys.stdout = self.saved_stdout

        sys.stderr.close()
        sys.stderr = self.saved_stderr

    def runApplication(self, params, code, err, out):
        
        # spusteni aplikace se zadanymi parametry
        with self.assertRaises(SystemExit) as e : 
            application.main(params)         
        
        # kontrola 
        assert e.exception.code == code
        assert bool(err) == bool(sys.stderr.getvalue())
        assert bool(out) == bool(sys.stdout.getvalue())
        
        # vrati vystup
        return sys.stdout.getvalue()
       
    def suite(self):

        suite = unittest.TestLoader().loadTestsFromTestCase(self)
        return suite