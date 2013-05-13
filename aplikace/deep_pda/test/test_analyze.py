'''
Testy funkce pro analyzu retezce.

@author: Vendula Poncova
'''
import unittest
from .test_case import Test

#####################################################################
class TestAnalyze(Test):
    
    path = "test/input/"

    def test(self):
        assert True

    def runAnalyze_ok(self, file, string, steps = 100):
        
        out = self.runApplication(["gdeep_analyze", 
                                   "--input=" + self.path + file, 
                                   "--analyze-string=" + string + "",
                                   "--max-steps=" + str(steps)], 
                                  0, 
                                  err = False, 
                                  out = True)
        
        return out

    def runAnalyze_err(self, file, string, steps = 100):
        
        out = self.runApplication(["gdeep_analyze", 
                                   "--input=" + self.path + file, 
                                   "--analyze-string=" + string + "",
                                   "--max-steps=" + str(steps)], 
                                  0, 
                                  err = True, 
                                  out = False)
        return out
      
            
    def test_ok_analyze_01(self):
                 
        for string in ("a b c", "a a b b c c", "a a a b b b c c c") :
            self.runAnalyze_ok("test_ok_01", string)
             
    def test_err_analyze_01(self):
                  
        for string in ("a a b c", "a a b b b c c", "a a a b b b c") :
            self.runAnalyze_err("test_ok_01", string)
 
    def test_ok_analyze_02(self):
          
        for string in ("a b c", "a a b b c c", "a a a b b b c c c") :
            self.runAnalyze_ok("test_ok_02", string)
  
    def test_err_analyze_02(self):
          
        for string in ("a b c c", "a b b c c", "a a a b b b b c c c") :
            self.runAnalyze_err("test_ok_02", string)
      
    def test_ok_analyze_03(self):
                 
        for string in ("á ů ž", "á á ů ů ž ž", "á á á ů ů ů ž ž ž") :
            self.runAnalyze_ok("test_ok_03", string)
 
    def test_err_analyze_03(self):
                 
        for string in ("ů ž", "á á ů ž ž", "á á á ů ů ů ž ž") :
            self.runAnalyze_err("test_ok_03", string)
      
    def test_ok_analyze_04(self):
         
        for string in ("á ů ž", "á á ů ů ž ž", "á á á ů ů ů ž ž ž") :           
            self.runAnalyze_ok("test_ok_04", string)
 
    def test_err_analyze_04(self):
         
        for string in ("á ů ů ů ž", "á á á ů ů ž ž", "á á á ů ů ů ž ž ž ž") :           
            self.runAnalyze_err("test_ok_04", string)
  
    def test_ok_analyze_05(self):
         
        for string in ("a b c", "a a b b c c", "a a a b b b c c c") :
            self.runAnalyze_ok("test_ok_05", string)
  
    def test_ok_analyze_06(self):
 
        for string in ("Agáta Bedřich Cecílie", 
                       "Agáta Agáta Bedřich Bedřich Cecílie Cecílie",
                        "Agáta Agáta Agáta Bedřich Bedřich Bedřich Cecílie Cecílie Cecílie") :
            self.runAnalyze_ok("test_ok_06", string)
          
    def test_ok_analyze_07(self):
         
        for string in ("a b c", "a a b b c c", "a a a b b b c c c") :
            self.runAnalyze_ok("test_ok_07", string)
          
    def test_ok_analyze_08(self):
        self.runAnalyze_ok("test_ok_08", "a a a")
         
    def test_err_analyze_08(self):
        self.runAnalyze_err("test_ok_08", "a a a a")
  
#     def test_ok_analyze_big_01(self):
#           
#         for string in ("a b c") : #, "a a b b c c", "a a a b b b c c c") :
#             self.runAnalyze_ok("test_ok_big_01", string, 200)
             
    def test_ok_analyze_states_01(self):
        self.runAnalyze_ok("test_ok_states_01", "a a a")
         
    def test_err_analyze_states_01(self):
        self.runAnalyze_err("test_ok_states_01", "a")
 
    def test_ok_analyze_states_02(self):
         
        for string in ("a b c", "a a b b c c", "a a a b b b c c c") :
            self.runAnalyze_ok("test_ok_states_02", string, 1000)
 
    def test_err_analyze_states_02(self):
         
        for string in ("a c", "a a b b c", "a a a b b b b c c c") :
            self.runAnalyze_err("test_ok_states_02", string, 1000)
         
    def test_ok_analyze_symbols_01(self):
        self.runAnalyze_ok("test_ok_symbols_01", "a a a")
 
    def test_err_analyze_symbols_01(self):
        self.runAnalyze_err("test_ok_symbols_01", "a a")
 
    def test_ok_analyze_symbols_02(self):        
        for string in ("a b c", "a a b b c c", "a a a b b b c c c") :
            self.runAnalyze_ok("test_ok_symbols_02", string, 1000)
 
    def test_err_analyze_symbols_02(self):        
        for string in ("a c", "a a b c c", "a a a b b b c c c c") :
            self.runAnalyze_err("test_ok_symbols_02", string, 1000)
    
##################################################################### konec souboru