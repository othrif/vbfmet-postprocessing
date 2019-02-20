class sample(object):
    def __init__(self,samplename="",syst="",Ext=False):
        self.sampleType=""
        self.sampleTypeList= []
        self.isMC=False
        self.runNumber=0
        self.runNumberS=""
        self.subfileN=""
        self.load(samplename,syst,Ext)
        self.sampleTypeList = ["W_EWK","W_strong","Z_EWK", "Z_strongPow", "Z_strongExt", "Z_strongPTVExt", "Z_strong_VBFFilt","Z_strong_LowMass","Z_strong","ttbar","VBFH125","ggFH125","VH125","VBFHOther","QCDw","QCDunw","VVV","VV","data"] # do not change order

        self.sampleMap = {'data':['data'],
                          'W_EWK':['W_EWK'],
                          'Z_EWK':['Z_EWK'],
                          'W_strong':['W_strong'],
                          'Z_strong':['Z_strong','Z_strong_VBFFilt','Z_strong_LowMass'],
                          'Z_strong_VBFFilt':['Z_strong_VBFFilt'],
                          'Z_strongExt':['Z_strongExt'],
                          'Z_strongPTVExt':['Z_strongPTVExt'],
                          'VV_VVV':['VV','VVV'],
                          'signal':['VBFH125','ggFH125','VH125'],
                          'VBFHOther':['VBFHOther'],
                          'QCD':['QCDw','QCDunw'],
                          }

    def load(self,samplename,syst,Ext):

        if samplename == "":
            return
        if syst == "":
            samplesplit = samplename.split(".")
            for p,s in enumerate(samplesplit):
                if s[0]=="v":
                    self.runNumber = int(samplesplit[p+1])
                    self.runNumberS = samplesplit[p+1]
                    break
            #print "RUN: ",self.runNumber
            if "MiniNtuple.root/user" in samplename:
                self.subfileN = samplename.split(".")[-3]
            if "physics_Main" in samplesplit:
                self.isMC = False
            else:
                self.isMC = True
        else:
            samplesplit = samplename.split("_")
            for p,s in enumerate(samplesplit):
                if syst in s:
                    self.runNumber = int(s[s.find(syst)+len(syst):])
                    self.runNumberS = s[s.find(syst)+len(syst):]
            if self.runNumberS+"_" in samplename:
                self.subfileN = samplename.split("_")[-1][:samplename.split("_")[-1].find(".root")]
            if "/data" in samplename:
                self.isMC = False
            else:
                self.isMC = True
        if (self.isMC):
            if ((self.runNumber >= 308096 and self.runNumber <= 308098) or (self.runNumber == 363489)):
                self.sampleType = "W_EWK"
            elif (self.runNumber >= 364156 and self.runNumber <= 364197):
                self.sampleType = "W_strong"
            elif (self.runNumber >= 363600 and self.runNumber <= 363671):
                self.sampleType = "W_strong" # madgraph
            elif (self.runNumber >= 308092 and self.runNumber <= 308095):
                self.sampleType = "Z_EWK"
            elif (self.runNumber >= 345099 and self.runNumber <= 345102):
                self.sampleType = "Z_strong_VBFFilt"
            elif (self.runNumber >= 364100 and self.runNumber <= 364155) or (self.runNumber <= 361519 and self.runNumber >= 361515):
                self.sampleType = "Z_strong"
            elif ((self.runNumber >= 410011 and self.runNumber <= 410014) or (self.runNumber == 410025) or (self.runNumber == 410026) or (self.runNumber == 410470) or (self.runNumber == 410471) or (self.runNumber == 410472)) or (self.runNumber>=410642 and self.runNumber<=410649) or self.runNumber==410642 or self.runNumber==410643:
                self.sampleType = "ttbar"
            elif ((self.runNumber == 308276) or (self.runNumber == 308567)):
                self.sampleType = "VBFH125"
            elif ((self.runNumber >= 308275) and self.runNumber <= 308283): 
                self.sampleType = "VBFHOther"
            elif (self.runNumber == 308284):
                self.sampleType = "ggFH125"
            elif ((self.runNumber == 308071) or (self.runNumber == 308072)):
                self.sampleType = "VH125"
            elif (self.runNumber >= 361020 and self.runNumber <= 361032) or self.runNumber==310502 or self.runNumber==304784:
                self.sampleType = "QCDw"
            elif (self.runNumber >= 426001 and self.runNumber <= 426009):
                self.sampleType = "QCDunw"
            elif (self.runNumber >= 364250 and self.runNumber <= 364255) or (self.runNumber >= 363355 and self.runNumber <= 363360) or self.runNumber==363489 or self.runNumber==363494:
                self.sampleType = "ttbar" # VV moved to ttbar+other
            elif (self.runNumber >= 364242 and self.runNumber <= 364249 or self.runNumber==364253):
                self.sampleType = "ttbar" # VVV moved to ttbar+other
            elif (self.runNumber >= 364198 and self.runNumber <= 364215):
                self.sampleType = "Z_strong" # Z_strong_LowMass added to the Z_strong
            elif (self.runNumber >= 301020 and self.runNumber <= 301038):
                self.sampleType = "Z_strongPow" #powheg
            elif (self.runNumber >=309665  and self.runNumber <= 309679):
                if Ext:
                    self.sampleType = "Z_strong" #extension
                else: 
                    self.sampleType = "Z_strongExt"
            elif (self.runNumber >=309662  and self.runNumber <= 309664):
                self.sampleType = "Z_strongExt"
            elif (self.runNumber >=364216  and self.runNumber <= 364229):
                self.sampleType = "Z_strongPTVExt" #other?
            elif (self.runNumber >= 363147 and self.runNumber <= 363170) or (self.runNumber >= 363123 and self.runNumber <= 363146) or (self.runNumber>=361510 and self.runNumber<=361519):
                self.sampleType = "Z_strong" #madgraph
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
    def getrunNumberS(self):
        return self.runNumberS
    def getsubfileN(self):
        return self.subfileN
    def getsampleTypeList(self):
        return self.sampleTypeList


  # we assume the samplename has the format user.**.v**.runNumber.
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
  # SingleTop: 410011-410014,410025,410026,ttbar:410470,410471,410472
  # Other higgs: 308275-308283                                                                                                                                                                                    
  #                                                                         
