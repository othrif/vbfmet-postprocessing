class sample(object):
    def __init__(self,samplename):
        self.sampleType=""
        self.isMC=False
        self.runNumber=0
        self.load(samplename)

    def load(self,samplename):
        samplesplit = samplename.split(".")
        for p,s in enumerate(samplesplit):
            if s[0]=="v":
                self.runNumber = int(samplesplit[p+1])

        if "physics_Main" in samplesplit:
            self.isMC = False
        else:
            self.isMC = True
        if (self.isMC):
            if ((self.runNumber >= 308096 and self.runNumber <= 308098) or (self.runNumber == 363359) or (self.runNumber == 363360) or (self.runNumber == 363489)):
                self.sampleType = "W_EWK"
            elif (self.runNumber >= 364156 and self.runNumber <= 364197):
                self.sampleType = "W_strong"
            elif ((self.runNumber >= 308092 and self.runNumber <= 308095) or (self.runNumber >= 363355 and self.runNumber <= 363358)):
                self.sampleType = "Z_EWK"
            elif (self.runNumber >= 364100 and self.runNumber <= 364155):
                self.sampleType = "Z_strong"
            elif ((self.runNumber >= 410011 and self.runNumber <= 410014) or (self.runNumber == 410025) or (self.runNumber == 410026) or (self.runNumber == 410470) or (self.runNumber == 410471)):
                self.sampleType = "ttbar"
            elif ((self.runNumber == 308276) or (self.runNumber == 308567)):
                self.sampleType = "VBFH125"
            elif (self.runNumber == 308284):
                self.sampleType = "ggFH125"
            elif ((self.runNumber == 308071) or (self.runNumber == 308072)):
                self.sampleType = "VH125"
            else:
                print "python/sample.py: runNumber "+str(self.runNumber)+" could not be identified as a valid MC :o"
                self.sampleType = "ERROR"
        else:
            self.sampleType = "data"

    def getisMC(self):
        return self.isMC
    def getsampleType(self):
        return self.sampleType
    def getrunNumber(self):
        return self.runNumber



  #                                                                                                                                                                                                               
  # Signal:  VBF: 308276,308567, ggF: 308284, VH: 308071,308072                                                                                                                                                   
  # Diboson: W: 363359-363360, 363489, Z: 363355-363358                                                                                                                                                           
  # Wenu:    strong 364170-364183, EWK 308096                                                                                                                                                                     
  # Wmunu:   strong 364156-364169, EWK 308097                                                                                                                                                                     
  # Wtaunu:  strong 364184-364197, EWK 308098                                                                                                                                                                     
  # Zee:     strong 364114-364127, EWK 308092                                                                                                                                                                     
  # Zmumu:   strong 364100-364113, EWK 308093                                                                                                                                                                     
  # Ztautau: strong 364128-364141, EWK 308094                                                                                                                                                                     
  # Znunu:   strong 364142-364155, EWK 308095                                                                                                                                                                     
  # SingleTop: 410011-410014,410025,410026,ttbar:410470,410471                                                                                                                                                    
  # Other higgs: 308275-308283                                                                                                                                                                                    
  #                                                                         
