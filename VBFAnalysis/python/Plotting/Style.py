import ROOT

def setLineAttr(self,color=1,style=1,width=1):
    self.SetLineColor(color)
    self.SetLineStyle(style)
    self.SetLineWidth(width)

def setFillAttr(self,color=1,style=3018):
    self.SetFillColor(color)
    self.SetFillStyle(style)

def setMarkerAttr(self,color=1,style=1,size=1):
    self.SetMarkerColor(color)
    self.SetMarkerStyle(style)
    self.SetMarkerSize(size)

def setStyles(self, styleList):
    setLineAttr(self,styleList[0],styleList[1],styleList[2])
    setFillAttr(self,styleList[3],styleList[4])
    setMarkerAttr(self,styleList[5],styleList[6],styleList[7])

# This dict defines the style for the histograms create by hist_from_file if the argument newTitle is a key
styleDict={}
    #processList=["hvh", "mqcd", "higgs", "vvv", "wewk", "hggf", "top2", 
    # "top1", "zewk", "data", "bkgs", "tall", "hvbf", "zldy", "dqcd", "zqcd", "wqcd"]

#0:LColor, 1:LStyle, 2:LWidth, 3:FColor, 4:FStyle, 5:MColor, 6:MStyle, 7:MSize

#channels [MJ, ttbar/VV/VVV, eFakes, Z EWK, W EWK, Z QCD, W QCD]
bold=[ROOT.kGreen+2,ROOT.kBlack,ROOT.kYellow,ROOT.kAzure-2,ROOT.kRed,ROOT.kBlue+1,ROOT.kRed+2]

pastels=[ROOT.kAzure-9,ROOT.kOrange-9,ROOT.kYellow-7,ROOT.kSpring+1,ROOT.kRed-7,ROOT.kGreen+3,ROOT.kRed-2]

#cool
#colors=[ROOT.kViolet-4,ROOT.kBlue-6,ROOT.kMagenta-10,ROOT.kSpring+8,ROOT.kTeal,ROOT.kGreen-2,ROOT.kCyan-3]
#colors=[ROOT.kMagenta-10,ROOT.kBlue-6,ROOT.kViolet-4,ROOT.kSpring+8,ROOT.kTeal,ROOT.kGreen-2,ROOT.kCyan-3]
colors=[ROOT.kMagenta-10,ROOT.kBlue-6,ROOT.kViolet-4,ROOT.kSpring+8,ROOT.kOrange+1,ROOT.kGreen-2,ROOT.kOrange+2]
#colors=[ROOT.kGray+1,ROOT.kBlue-6,ROOT.kMagenta-10,ROOT.kSpring+8,ROOT.kTeal,ROOT.kGreen-2,ROOT.kCyan-3]

warm=[ROOT.kOrange-1,ROOT.kOrange-9,ROOT.kYellow-7,ROOT.kOrange-3,ROOT.kRed-7,ROOT.kOrange+10,ROOT.kRed-2]

styleDict["bkgs"]=[1,1,2,0,0,0,0,0]
styleDict["data"]=[1,0,2,0,0,1,20,1.2]
styleDict["signal"]=[2,2,3,0,0,2,0,0] #ROOT.kOrange
styleDict["signalH"]=[2,2,2,0,0,0,0,0]

styleDict["Znunu"]=[3,1,1,3,1001,0,0,0]
styleDict["Wtaunu"]=[4,1,1,4,1001,0,0,0]
styleDict["Wmunu"]=[5,1,1,5,1001,0,0,0]
styleDict["ZnunuEWK"]=[6,1,1,6,1001,0,0,0]
styleDict["WEWK"]=[ROOT.kCyan   -9,1,1,ROOT.kCyan   -9,1001,ROOT.kCyan   -9,0,0]
styleDict["Wenu"]=[8,1,1,8,1001,0,0,0]
styleDict["top"]=[9,1,1,9,1001,0,0,0]
styleDict["Zmumu"]=[28,1,1,28,1001,0,0,0]
styleDict["Ztautau"]=[30,1,1,30,1001,0,0,0]
styleDict["VV"]=[34,1,1,34,1001,0,0,0]
styleDict["ZEWK"]=[ROOT.kBlue-9,1,1,ROOT.kBlue-9,1001,ROOT.kBlue-9,0,0]
styleDict["Zee"]=[46,1,1,46,1001,0,0,0]
styleDict["QCDw"]=[47,1,1,47,1001,0,0,0]
styleDict["SinglePhoton"]=[47,1,1,47,1001,0,0,0]
styleDict["multijet"]=[ROOT.kOrange-5,1,1,ROOT.kOrange-5,1001,ROOT.kOrange-5,0,0]
styleDict["Others"]=[49,1,1,49,1001,49,0,0]
styleDict["EFakePh"]=[49,1,1,49,1001,49,0,0]
styleDict["JetFakePh"]=[49,1,1,49,1001,49,0,0]
styleDict["ttbar"]=[49,1,1,49,1001,49,0,0]
styleDict["ttg"]=[49,1,1,49,1001,49,0,0]
#styleDict["ttbar"]=[ROOT.kMagenta-9,1,1,ROOT.kMagenta-9,1001,ROOT.kMagenta-9,0,0]
styleDict["ttbar"]=[colors[1],1,1,colors[1],1001,colors[1],0,0]
#styleDict["eleFakes"]=[43,1,1,43,1001,43,0,0]
styleDict["eleFakes"]=[colors[2],1,1,colors[2],1001,colors[2],0,0]
styleDict["muoFakes"]=[colors[2],1,1,colors[2],1001,colors[2],0,0]
styleDict["efakegam"]=[colors[2],1,1,colors[2],1001,colors[2],0,0]
styleDict["jfakegam"]=[colors[2],1,1,colors[2],1001,colors[2],0,0]

styleDict["Zjets"]=[4,1,1,4,1001,0,0,0]
styleDict["Wjets"]=[5,1,1,5,1001,0,0,0]
styleDict["nonVjets"]=[6,1,1,6,1001,0,0,0]

styleDict["VBFH125"]=[2,1,3,0,0,2,0,0]
styleDict["GGFH125"]=[2,2,3,0,0,2,0,0]
styleDict["ggFH125"]=[2,2,3,0,0,2,0,0]
styleDict["VH125"]=[2,3,3,0,0,2,0,0]


styleDict["W_strong"]=[ROOT.kGreen  -7,1,1,ROOT.kGreen  -7,1001,ROOT.kGreen  -7,0,0]
styleDict["Z_strong"]=[ROOT.kGreen  -3,1,1,ROOT.kGreen  -3,1001,ROOT.kGreen  -3,0,0]
styleDict["Wg_strong"]=[ROOT.kGreen  -7,1,1,ROOT.kGreen  -7,1001,ROOT.kGreen  -7,0,0]
styleDict["Zg_strong"]=[ROOT.kGreen  -3,1,1,ROOT.kGreen  -3,1001,ROOT.kGreen  -3,0,0]
styleDict["Z_EWK"]=[ROOT.kBlue-9,1,1,ROOT.kBlue-9,1001,ROOT.kBlue-9,0,0]
styleDict["W_EWK"]=[ROOT.kCyan   -9,1,1,ROOT.kCyan   -9,1001,ROOT.kCyan   -9,0,0]
styleDict["Zg_EWK"]=[ROOT.kBlue-9,1,1,ROOT.kBlue-9,1001,ROOT.kBlue-9,0,0]
styleDict["Wg_EWK"]=[ROOT.kCyan   -9,1,1,ROOT.kCyan   -9,1001,ROOT.kCyan   -9,0,0]
"""
styleDict["W_EWK"]=[ROOT.kGreen  -7,1,1,ROOT.kGreen  -7,1001,ROOT.kGreen  -7,0,0]
styleDict["W_strong"]=[ROOT.kGreen  -3,1,1,ROOT.kGreen  -3,1001,ROOT.kGreen  -3,0,0]
styleDict["Z_strong"]=[ROOT.kBlue-9,1,1,ROOT.kBlue-9,1001,ROOT.kBlue-9,0,0]
styleDict["Z_EWK"]=[ROOT.kCyan   -9,1,1,ROOT.kCyan   -9,1001,ROOT.kCyan   -9,0,0]
#styleDict["Z_strong"]=[1,1,1,46,1001,0,0,0]
#styleDict["Z_EWK"]=[1,1,1,8,1001,0,0,0]
#styleDict["W_EWK"]=[1,1,1,5,1001,0,0,0]
#styleDict["W_strong"]=[1,1,1,9,1001,0,0,0]
#styleDict["ttbar"]=[1,1,1,0,1001,0,0,0]
styleDict["multijet"]=[ROOT.kGray+1,1,1,ROOT.kGray+1,1001,ROOT.kGray+1,0,0]
"""
styleDict["W_EWK"]=[colors[4],1,1,colors[4],1001,colors[4],0,0]
styleDict["W_strong"]=[colors[6],1,1,colors[6],1001,colors[6],0,0]
styleDict["Z_strong"]=[colors[5],1,1,colors[5],1001,colors[5],0,0]
styleDict["Z_EWK"]=[colors[3],1,1,colors[3],1001,colors[3],0,0]
styleDict["multijet"]=[colors[0],1,1,colors[0],1001,colors[0],0,0]

# Define the binning for each variable
varBinning={}
# Bin edges for different variables
varBinning["jj_mass"]=[1e6, 1.5e6, 2e6, 5e6]
varBinning["jj_deta"]=[3+x*0.2 for x in range(30)]
varBinning["jj_dphi"]=[x*0.2 for x in range(18)]
varBinning["jet1_pt"]=[6e4+x*2e4 for x in range(40)]
varBinning["jet2_pt"]=[3e4+x*2e4 for x in range(20)]
varBinning["met"]=[1.3e5+x*2e4 for x in range(40)]

variables=[v for v in varBinning]

cutflow={}
sameForAll=["allEntries","passJetCleanTight","n_jet==2","j1_pt","j2_pt","jj_mass","jj_deta","jj_dphi","mht","met","n_el","n_mu","dphi(j1,met)","dphi(j2,met)","hemispheres"]
cutflow["sr"]=sameForAll+["trigger_met"]
cutflow["wcr"]=sameForAll+["trigger_lep","lep1","met_sig","charge"]
cutflow["zcr"]=sameForAll+["trigger_lep","lep1","lep2","mll","SFOS"]
