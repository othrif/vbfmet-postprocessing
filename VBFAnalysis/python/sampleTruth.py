class sample(object):
    def __init__(self,samplename="",syst=""):
        self.sampleType=""
        self.sampleTypeList= []
        self.isMC=False
        self.runNumber=0
        self.runNumberS=""
        self.subfileN=""
        self.load(samplename,syst)
        self.sampleTypeList = ["W_EWK","W_strong","Z_EWK", "Z_strong_VBFFilt","Z_strong_LowMass","Z_strong","ttbar","VBFH125","ggFH125","VH125","QCDw","QCDunw","VVV","VV","data"] # do not change order

        self.sampleMap = {'data':['data'],
                          'W_EWK':['W_EWK'],
                          'Z_EWK':['Z_EWK'],
                          'W_strong':['W_strong'],
                          'Z_strong':['Z_strong','Z_strong_VBFFilt','Z_strong_LowMass'],
                          'Z_strong_VBFFilt':['Z_strong_VBFFilt'],
                          'VV_VVV':['VV','VVV'],
                          'signal':['VBFH125','ggFH125','VH125'],
                          'QCD':['QCDw','QCDunw'],
                          }

    def load(self,samplename,syst):
        W_ckkw15        = [362384, 362392, 362400, 362408, 362416, 362424, 362432, 362440, 362448, 362456, 362464, 362472, 362480, 362488, 362496, 362504, 362512, 362520, 362528, 362536, 362544, 362552, 362560, 362568]
        W_ckkw30        = [362385, 362401, 362409, 362417, 362425, 362433, 362441, 362449, 362457, 362465, 362473, 362481, 362489, 362497, 362505, 362513, 362521, 362529, 362537, 362545, 362553, 362561, 362569]
        W_qsf025        = [362390, 362398, 362406, 362414, 362422, 362430, 362438, 362446, 362454, 362462, 362470, 362478, 362486, 362494, 362502, 362510, 362518, 362526, 362534, 362542, 362550, 362558, 362566, 362574]
        W_qsf4          = [362391, 362399, 362407, 362423, 362431, 362439, 362447, 362455, 362463, 362471, 362479, 362487, 362495, 362503, 362511, 362519, 362527, 362535, 362543, 362551, 362559, 362567, 362575]
        Zee_ckkw15      = [362192, 362200, 362208, 362216, 362224, 362232, 362240, 362248, 362256, 362264, 362272, 362280, 362288, 362296, 362304, 362312, 362320, 362328, 362336, 362344, 362352, 362360, 362368, 362376]
        Zee_ckkw30      = [362193, 362201, 362209, 362217, 362225, 362233, 362241, 362249, 362257, 362265, 362273, 362281, 362289, 362297, 362305, 362313, 362321, 362329, 362337, 362345, 362353, 362361, 362369, 362377]
        Zee_qsf025      = [362198, 362206, 362214, 362222, 362230, 362238, 362246, 362254, 362262, 362270, 362278, 362286, 362294, 362302, 362310, 362318, 362326, 362334, 362342, 362350, 362358, 362366, 362374, 362382]
        Zee_qsf4        = [362199, 362207, 362215, 362223, 362231, 362239, 362247, 362255, 362263, 362271, 362279, 362287, 362295, 362303, 362311, 362319, 362327, 362335, 362343, 362351, 362359, 362367, 362375, 362383]
        Znunu_ckkw15    = [362000, 362008, 362016, 362024, 362032, 362040, 362048, 362056, 362064, 362072, 362080, 362088, 362096, 362104, 362112, 362120, 362128, 362136, 362144, 362152, 362160, 362168, 362176, 362184]
        Znunu_ckkw30    = [362001, 362009, 362017, 362025, 362033, 362041, 362049, 362057, 362065, 362073, 362081, 362089, 362097, 362105, 362113, 362121, 362129, 362137, 362145, 362153, 362161, 362169, 362177, 362185]
        Znunu_qsf025    = [362006, 362014, 362022, 362030, 362038, 362046, 362054, 362062, 362070, 362078, 362086, 362094, 362102, 362110, 362118, 362126, 362134, 362142, 362150, 362158, 362166, 362174, 362182, 362190]
        Znunu_qsf4      = [362007, 362015, 362023, 362031, 362039, 362047, 362055, 362063, 362071, 362079, 362087, 362095, 362103, 362111, 362119, 362127, 362135, 362143, 362151, 362159, 362167, 362175, 362183, 362191]

        if samplename == "":
            return
        if syst == "":
            samplesplit = samplename.split(".")
            for p,s in enumerate(samplesplit):
                if s[0]=="v":
                    self.runNumber = int(samplesplit[p+1])
                    self.runNumberS = samplesplit[p+1]
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
            if (self.runNumber == 305178):
                self.sampleType = "W_EWK_ckkw15"
            elif (self.runNumber == 305179):
                self.sampleType = "W_EWK_ckkw30"
            elif (self.runNumber == 305184):
                self.sampleType = "W_EWK_qsf025"
            elif (self.runNumber == 305185):
                self.sampleType = "W_EWK_qsf4"
            elif (self.runNumber in W_ckkw15):
                self.sampleType = "W_strong_ckkw15"
            elif (self.runNumber in W_ckkw30):
                self.sampleType = "W_strong_ckkw30"
            elif (self.runNumber in W_qsf025):
                self.sampleType = "W_strong_qsf025"
            elif (self.runNumber in W_qsf4):
                self.sampleType = "W_strong_qsf4"
            elif (self.runNumber == 305194 or self.runNumber == 305186):
                self.sampleType = "Z_EWK_ckkw15"
            elif (self.runNumber == 305195 or self.runNumber == 305187):
                self.sampleType = "Z_EWK_ckkw30"
            elif (self.runNumber == 305200 or self.runNumber == 305192):
                self.sampleType = "Z_EWK_qsf025"
            elif (self.runNumber == 305201 or self.runNumber == 305193):
                self.sampleType = "Z_EWK_qsf4"
            elif (self.runNumber in Zee_ckkw15 or self.runNumber in Znunu_ckkw15):
                self.sampleType = "Z_strong_ckkw15"
            elif (self.runNumber in Zee_ckkw30 or self.runNumber in Znunu_ckkw30):
                self.sampleType = "Z_strong_ckkw30"
            elif (self.runNumber in Zee_qsf025 or self.runNumber in Znunu_qsf025):
                self.sampleType = "Z_strong_qsf025"
            elif (self.runNumber in Zee_qsf4 or self.runNumber in Znunu_qsf4):
                self.sampleType = "Z_strong_qsf4"
            elif ((self.runNumber >= 364100 and self.runNumber <= 364155)):
#                self.sampleType = "Z_strong_MAXHTPTV"
                self.sampleType = "Z_strong"
            elif ((self.runNumber >= 364156 and self.runNumber <= 364197)):
                #self.sampleType = "W_strong_MAXHTPTV"
                self.sampleType = "W_strong"
            elif ((self.runNumber >= 312448 and self.runNumber <= 312495) or (self.runNumber >= 364216 and self.runNumber <= 364223)):
                #self.sampleType = "Z_strong_KTPTV"
                self.sampleType = "Z_strong"
            elif ((self.runNumber >= 312496 and self.runNumber <= 312531) or (self.runNumber >= 364224 and self.runNumber <= 364229)):
                #self.sampleType = "W_strong_KTPTV"
                self.sampleType = "W_strong"
            elif ((self.runNumber >= 361372 and self.runNumber <= 361379)):
                #self.sampleType = "Z_strong_KTPTV"
                self.sampleType = "Z_strong_211"
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
  # SingleTop: 410011-410014,410025,410026,ttbar:410470,410471
  # Other higgs: 308275-308283
  #
  # Variations
  #
  # Wenu_ckkw15:    EWK 305178, strong 362384, 362392, 362400, 362408, 362416, 362424, 362432, 362440, 362448, 362456, 362464, 362472, 362480, 362488, 362496, 362504, 362512, 362520, 362528, 362536, 362544, 362552, 362560, 362568
  # Wenu_ckkw30:    EWK 305179, strong 362385, 362401, 362409, 362417, 362425, 362433, 362441, 362449, 362457, 362465, 362473, 362481, 362489, 362497, 362505, 362513, 362521, 362529, 362537, 362545, 362553, 362561, 362569
  # Wenu_qsf025:    EWK 305184, strong 362390, 362398, 362406, 362414, 362422, 362430, 362438, 362446, 362454, 362462, 362470, 362478, 362486, 362494, 362502, 362510, 362518, 362526, 362534, 362542, 362550, 362558, 362566, 362574
  # Wenu_qsf4:      EWK 305185, strong 362391, 362399, 362407, 362423, 362431, 362439, 362447, 362455, 362463, 362471, 362479, 362487, 362495, 362503, 362511, 362519, 362527, 362535, 362543, 362551, 362559, 362567, 362575
  # Zee_ckkw15:     EWK 305194, strong 362192, 362200, 362208, 362216, 362224, 362232, 362240, 362248, 362256, 362264, 362272, 362280, 362288, 362296, 362304, 362312, 362320, 362328, 362336, 362344, 362352, 362360, 362368, 362376
  # Zee_ckkw30:     EWK 305195, strong 362193, 362201, 362209, 362217, 362225, 362233, 362241, 362249, 362257, 362265, 362273, 362281, 362289, 362297, 362305, 362313, 362321, 362329, 362337, 362345, 362353, 362361, 362369, 362377
  # Zee_qsf025:     EWK 305200, strong 362198, 362206, 362214, 362222, 362230, 362238, 362246, 362254, 362262, 362270, 362278, 362286, 362294, 362302, 362310, 362318, 362326, 362334, 362342, 362350, 362358, 362366, 362374, 362382
  # Zee_qsf4:       EWK 305201, strong 362199, 362207, 362215, 362223, 362231, 362239, 362247, 362255, 362263, 362271, 362279, 362287, 362295, 362303, 362311, 362319, 362327, 362335, 362343, 362351, 362359, 362367, 362375, 362383
  # Znunu_ckkw15:   EWK 305186, strong 362000, 362008, 362016, 362024, 362032, 362040, 362048, 362056, 362064, 362072, 362080, 362088, 362096, 362104, 362112, 362120, 362128, 362136, 362144, 362152, 362160, 362168, 362176, 362184
  # Znunu_ckkw30:   EWK 305187, strong 362001, 362009, 362017, 362025, 362033, 362041, 362049, 362057, 362065, 362073, 362081, 362089, 362097, 362105, 362113, 362121, 362129, 362137, 362145, 362153, 362161, 362169, 362177, 362185
  # Znunu_qsf025:   EWK 305192, strong 362006, 362014, 362022, 362030, 362038, 362046, 362054, 362062, 362070, 362078, 362086, 362094, 362102, 362110, 362118, 362126, 362134, 362142, 362150, 362158, 362166, 362174, 362182, 362190
  # Znunu_qsf4:     EWK 305193, strong 362007, 362015, 362023, 362031, 362039, 362047, 362055, 362063, 362071, 362079, 362087, 362095, 362103, 362111, 362119, 362127, 362135, 362143, 362151, 362159, 362167, 362175, 362183, 362191
