import ROOT
import math
import sys
# create output
ROOT.gROOT.ProcessLine(
"struct MyStruct {\
   Float_t   jj_mass;\
   Float_t   jj_dphi;\
   Float_t   jj_deta;\
   Float_t   w;\
   Float_t   met_tenacious_tst_j1_dphi;\
   Float_t   met_tenacious_tst_j2_dphi;\
   Float_t   met_tenacious_tst_et;\
   Float_t   met_tenacious_tst_phi;\
   Float_t   met_cst_jet;\
   Float_t   met_soft_tst_et;\
   Float_t   met_significance;\
   Float_t   max_mj_over_mjj;\
   Float_t   maxCentrality;\
   std::vector<Float_t>   *jet_pt;\
   std::vector<Float_t>   *jet_eta;\
   std::vector<Float_t>   *jet_phi;\
   std::vector<Float_t>   *jet_m;\
   std::vector<Float_t>   *jet_timing;\
   std::vector<Float_t>   *jet_jvt;\
   std::vector<Float_t>   *jet_fjvt;\
   std::vector<unsigned short>   *jet_NTracks;\
   Int_t     n_vx;\
   Int_t     n_tau;\
   Int_t     n_el;\
   Int_t     n_ph;\
   Int_t     n_mu;\
   Int_t     n_baseel;\
   Int_t     n_basemu;\
   Int_t     n_jet;\
   Int_t     n_bjet;\
   Int_t     trigger_met;\
   Int_t     trigger_lep;\
   Int_t     runNumber;\
   Int_t     trigger_met_encoded;\
   Int_t     trigger_met_encodedv2;\
   Bool_t     passVjetsFilter;\
   Bool_t     passVjetsPTV;\
   Int_t     passJetCleanTight;\
   Float_t   met_tst_phi;\
   Float_t   met_tst_nolep_phi;\
   Float_t   met_soft_tst_phi;\
   Float_t   met_soft_tst_sumet;\
   Float_t   met_tight_tst_et;\
   Float_t   met_tight_tst_phi;\
   Float_t   met_truth_et;\
   Float_t   met_tst_et;\
   Float_t   met_tst_j1_dphi;\
   Float_t   met_tst_j2_dphi;\
   Float_t   met_tst_nolep_et;\
   Float_t   met_tst_nolep_j1_dphi;\
   Float_t   met_tst_nolep_j2_dphi;\
   Float_t   metsig_tst;\
   Float_t   averageIntPerXing;\
   ULong64_t     eventNumber;\
};" );

flts=['met_soft_tst_phi',
  'met_soft_tst_sumet',
  'met_tight_tst_et',
  'met_tight_tst_phi',
  'met_truth_et',
  'met_tst_et',
  'met_tst_j1_dphi',
  'met_tst_j2_dphi',
  'met_tst_nolep_et',
  'met_tst_nolep_j1_dphi',
  'met_tst_nolep_j2_dphi',
  'met_tst_nolep_phi',
  'met_tst_phi',
  'metsig_tst',]
ints =['passJetCleanTight',
  'trigger_met_encoded',
  'trigger_met_encodedv2',]
bols=[  'passVjetsFilter',
  'passVjetsPTV',]
from ROOT import MyStruct
mystruct = MyStruct()
tree_out = ROOT.TTree( 'QCDDDNominal', 'Nominal data driven QCD' )
#tree_out.Branch( 'myfloats', mystruct, 'jj_mass/F:jj_dphi/F:jj_deta/F' )
tree_out.Branch( 'jj_mass', ROOT.AddressOf( mystruct, 'jj_mass' ), 'jj_mass/F' )
tree_out.Branch( 'jj_dphi', ROOT.AddressOf( mystruct, 'jj_dphi' ), 'jj_dphi/F' )
tree_out.Branch( 'jj_deta', ROOT.AddressOf( mystruct, 'jj_deta' ), 'jj_deta/F' )
tree_out.Branch( 'w', ROOT.AddressOf( mystruct, 'w' ), 'w/F' )
tree_out.Branch( 'met_tenacious_tst_j1_dphi', ROOT.AddressOf( mystruct, 'met_tenacious_tst_j1_dphi' ), 'met_tenacious_tst_j1_dphi/F' )
tree_out.Branch( 'met_tenacious_tst_j2_dphi', ROOT.AddressOf( mystruct, 'met_tenacious_tst_j2_dphi' ), 'met_tenacious_tst_j2_dphi/F' )
tree_out.Branch( 'met_tenacious_tst_et', ROOT.AddressOf( mystruct, 'met_tenacious_tst_et' ), 'met_tenacious_tst_et/F' )
tree_out.Branch( 'met_tenacious_tst_phi', ROOT.AddressOf( mystruct, 'met_tenacious_tst_phi' ), 'met_tenacious_tst_phi/F' )
tree_out.Branch( 'met_cst_jet', ROOT.AddressOf( mystruct, 'met_cst_jet' ), 'met_cst_jet/F' )
tree_out.Branch( 'met_soft_tst_et', ROOT.AddressOf( mystruct, 'met_soft_tst_et' ), 'met_soft_tst_et/F' )
tree_out.Branch( 'met_significance', ROOT.AddressOf( mystruct, 'met_significance' ), 'met_significance/F' )
tree_out.Branch( 'max_mj_over_mjj', ROOT.AddressOf( mystruct, 'max_mj_over_mjj' ), 'max_mj_over_mjj/F' )
tree_out.Branch( 'maxCentrality', ROOT.AddressOf( mystruct, 'maxCentrality' ), 'maxCentrality/F' )
tree_out.Branch( 'n_vx', ROOT.AddressOf( mystruct, 'n_vx' ), 'n_vx/I' )
tree_out.Branch( 'n_tau', ROOT.AddressOf( mystruct, 'n_tau' ), 'n_tau/I' )
#tree_out.Branch( 'n_pv', ROOT.AddressOf( mystruct, 'n_pv' ), 'n_pv/I' )
tree_out.Branch( 'n_el', ROOT.AddressOf( mystruct, 'n_el' ), 'n_el/I' )
tree_out.Branch( 'n_ph', ROOT.AddressOf( mystruct, 'n_ph' ), 'n_ph/I' )
tree_out.Branch( 'n_mu', ROOT.AddressOf( mystruct, 'n_mu' ), 'n_mu/I' )
tree_out.Branch( 'n_baseel', ROOT.AddressOf( mystruct, 'n_baseel' ), 'n_baseel/I' )
tree_out.Branch( 'n_basemu', ROOT.AddressOf( mystruct, 'n_basemu' ), 'n_basemu/I' )
tree_out.Branch( 'n_jet', ROOT.AddressOf( mystruct, 'n_jet' ), 'n_jet/I' )
tree_out.Branch( 'n_bjet', ROOT.AddressOf( mystruct, 'n_bjet' ), 'n_bjet/I' )
tree_out.Branch( 'trigger_met', ROOT.AddressOf( mystruct, 'trigger_met' ), 'trigger_met/I' )
tree_out.Branch( 'trigger_lep', ROOT.AddressOf( mystruct, 'trigger_lep' ), 'trigger_lep/I' )
tree_out.Branch( 'runNumber', ROOT.AddressOf( mystruct, 'runNumber' ), 'runNumber/I' )
tree_out.Branch( 'averageIntPerXing', ROOT.AddressOf( mystruct, 'averageIntPerXing' ), 'averageIntPerXing/F' )
tree_out.Branch( 'eventNumber', ROOT.AddressOf( mystruct, 'eventNumber' ), 'eventNumber/l' )
for v in flts:
    tree_out.Branch( v, ROOT.AddressOf( mystruct, v ), v+'/F' )
for v in bols:
    tree_out.Branch( v, ROOT.AddressOf( mystruct, v ), v+'/O' )
for v in ints:
    tree_out.Branch( v, ROOT.AddressOf( mystruct, v ), v+'/I' )
mystruct.jet_pt = ROOT.std.vector('float')()
mystruct.jet_eta = ROOT.std.vector('float')()
mystruct.jet_phi = ROOT.std.vector('float')()
mystruct.jet_m = ROOT.std.vector('float')()
mystruct.jet_timing = ROOT.std.vector('float')()
mystruct.jet_jvt = ROOT.std.vector('float')()
mystruct.jet_fjvt = ROOT.std.vector('float')()
mystruct.jet_NTracks = ROOT.std.vector('unsigned short')()

tree_out.Branch( 'jet_pt',  mystruct.jet_pt)
tree_out.Branch( 'jet_eta', mystruct.jet_eta)
tree_out.Branch( 'jet_phi', mystruct.jet_phi)
tree_out.Branch( 'jet_m', mystruct.jet_m)
tree_out.Branch( 'jet_timing', mystruct.jet_timing)
tree_out.Branch( 'jet_jvt', mystruct.jet_jvt)
tree_out.Branch( 'jet_fjvt', mystruct.jet_fjvt)
tree_out.Branch( 'jet_NTracks', mystruct.jet_NTracks)
#tree_out.Branch( 'jet_phi', ROOT.AddressOf( mystruct, 'jet_phi' ), 'jet_phi' )
#tree_out.Branch( 'jet_m', ROOT.AddressOf( mystruct, 'jet_m' ), 'jet_m' )
#tree_out.Branch( 'jet_timing', ROOT.AddressOf( mystruct, 'jet_timing' ), 'jet_timing' )
#tree_out.Branch( 'jet_jvt', ROOT.AddressOf( mystruct, 'jet_jvt' ), 'jet_jvt' )
#tree_out.Branch( 'jet_fjvt', ROOT.AddressOf( mystruct, 'jet_fjvt' ), 'jet_fjvt' )
#tree_out.Branch( 'jet_NTracks', ROOT.AddressOf( mystruct, 'jet_NTracks' ), 'jet_NTracks' )
 
#f = ROOT.TFile.Open('/eos/atlas/atlascerngroupdisk/penn-ww/out_QCD_Tenacious.root')
#f = ROOT.TFile.Open('out_QCD_Tenacious.root')
#f = ROOT.TFile.Open('out_QCD_Loose.root')
f = ROOT.TFile.Open('mj2018.root')
IsLoose=False

GeV=1.0e3
tree = f.Get('PredictionTree')
fout = ROOT.TFile.Open('foutLoose.root','RECREATE')
z=0
v1 = ROOT.TLorentzVector()
v2 = ROOT.TLorentzVector()
v3 = ROOT.TLorentzVector()
v4 = ROOT.TLorentzVector()
met = ROOT.TLorentzVector()

h1= ROOT.TH1F("cutflow","cutflow",20, 0.5, 20.5)
h1.SetDirectory(fout)
#tree_out.SetDirectory(fout)
print 'Total: ',tree.GetEntries()
for e in tree:
    if z%10000 ==0:
        print 'Event: ',z
        sys.stdout.flush()
    #if z>100000:
    #    break
    z+=1
    
    # remove those with ntries not >0. -2 is the unsmeared events
    if e.Ntries<0.2:
        continue

    # weight is trigger and event  
    # and divide by 20, which is the number of pseudo samples
    weight = e.Weight*e.TriggerWeight/20.0 #/36100.0

    if not (e.JetPt[0]>70.0):
        continue
    if not (e.JetPt[1]>40.0):
        continue
    # apply MET cuts
    if not (e.MET>100.0):
        continue
    # counting njet
    mystruct.n_jet=0
    allJets=0
    for jetPt in e.JetPt:
        allJets+=1
        if jetPt>25.0:
            mystruct.n_jet+=1
    minNjet = min(5,mystruct.n_jet)
    
    # apply jet cut
    if mystruct.n_jet>4 or mystruct.n_jet<2:
        continue
    h1.Fill(2, weight)

    mystruct.jet_pt.clear();
    mystruct.jet_eta.clear();
    mystruct.jet_phi.clear();
    mystruct.jet_m.clear();
    mystruct.jet_timing.clear();
    mystruct.jet_jvt.clear();
    mystruct.jet_fjvt.clear();
    mystruct.jet_NTracks.clear();    
    ijetUsed=0
    for i in range(0,allJets):
        if not (e.JetPt[i]>25.0):
            continue
        mystruct.jet_pt.push_back(e.JetPt[i]*GeV)
        mystruct.jet_eta.push_back(e.JetEta[i])
        mystruct.jet_phi.push_back(e.JetPhi[i])
        mystruct.jet_m.push_back(e.JetM[i]*GeV)
        mystruct.jet_timing.push_back(0.0)
        mystruct.jet_jvt.push_back(e.JetJVT[i])
        mystruct.jet_NTracks.push_back(e.JetNTracks[i])
        if IsLoose:
            mystruct.jet_fjvt.push_back(0.0)
        else:
            mystruct.jet_fjvt.push_back(e.JetFJVT[i])
    
    # jet cuts
    met.SetPtEtaPhiM(e.MET, 0.0, e.METphi, 0.0)
    v1.SetPtEtaPhiM(mystruct.jet_pt[0],mystruct.jet_eta[0],mystruct.jet_phi[0],mystruct.jet_m[0])
    v2.SetPtEtaPhiM(mystruct.jet_pt[1],mystruct.jet_eta[1],mystruct.jet_phi[1],mystruct.jet_m[1])
    if mystruct.n_jet>2:
        v3.SetPtEtaPhiM(mystruct.jet_pt[2],mystruct.jet_eta[2],mystruct.jet_phi[2],mystruct.jet_m[2])
    if mystruct.n_jet>3:
        v4.SetPtEtaPhiM(mystruct.jet_pt[3],mystruct.jet_eta[3],mystruct.jet_phi[3],mystruct.jet_m[3])

    # compute vars
    #j1_met_dphi=3
    #j2_met_dphi=3
    j1_met_dphi = abs(v1.DeltaPhi(met))
    j2_met_dphi = abs(v2.DeltaPhi(met))
    jj_deta = abs(mystruct.jet_eta[0] - mystruct.jet_eta[1])
    jj_dphi = abs(v1.DeltaPhi(v2))
    # dphijj cut
    if jj_dphi >1.8:
        continue
    
    #jj_dphi=5
    jj_mass = (v1+v2).M()
    # write output tree
    mystruct.jj_mass = jj_mass
    mystruct.jj_dphi = jj_dphi
    mystruct.jj_deta = jj_deta
    mystruct.w = weight
    mystruct.met_tenacious_tst_j1_dphi = j1_met_dphi
    mystruct.met_tenacious_tst_j2_dphi = j2_met_dphi
    mystruct.met_tenacious_tst_et = e.MET*GeV
    mystruct.met_tenacious_tst_phi = e.METphi
    mystruct.met_cst_jet = e.MHTDefReb*GeV # MHT includes the soft term. 
    mystruct.met_soft_tst_et = e.METsoft*GeV
    mystruct.met_significance=e.METsig
    mystruct.max_mj_over_mjj=-9999.0
    mystruct.maxCentrality=-9999.0
    mystruct.trigger_met_encoded=1
    mystruct.trigger_met_encodedv2=1
    mystruct.passVjetsFilter=1
    mystruct.passVjetsPTV=1
    mystruct.passJetCleanTight=1
    mystruct.met_tst_phi = e.METphi
    mystruct.met_tst_nolep_phi = e.METphi
    mystruct.met_soft_tst_phi=0.0
    mystruct.met_soft_tst_sumet=0.0
    mystruct.met_tight_tst_et = e.MET*GeV
    mystruct.met_tight_tst_phi = e.METphi
    mystruct.met_truth_et=0
    mystruct.met_tst_et = e.MET*GeV
    mystruct.met_tst_j1_dphi = j1_met_dphi
    mystruct.met_tst_j2_dphi = j2_met_dphi
    mystruct.met_tst_nolep_et = e.MET*GeV
    mystruct.met_tst_nolep_j1_dphi = j1_met_dphi
    mystruct.met_tst_nolep_j2_dphi = j2_met_dphi
    mystruct.metsig_tst=e.METsig
            
    #print minNjet
    for j in range(2,minNjet):
        centrality = math.exp(-4.0/jj_deta**2 * (mystruct.jet_eta[j] - (mystruct.jet_eta[0]+mystruct.jet_eta[1])/2.0)**2);
        if centrality>mystruct.maxCentrality:
            mystruct.maxCentrality = centrality
        if j==2:
            mj1 = (v1+v3).M()
            mj2 = (v2+v3).M()
            maxmj3_over_mjj = min(mj1,mj2)/jj_mass;
            mystruct.max_mj_over_mjj = max(mystruct.max_mj_over_mjj, maxmj3_over_mjj)
            #print '3 jet: ', maxmj3_over_mjj,  mystruct.max_mj_over_mjj            
        elif j==3:
            mj1 = (v1+v4).M()
            mj2 = (v2+v4).M()
            maxmj3_over_mjj = min(mj1,mj2)/jj_mass;
            mystruct.max_mj_over_mjj = max(mystruct.max_mj_over_mjj, maxmj3_over_mjj)
            #print '4jet: ', maxmj3_over_mjj,  mystruct.max_mj_over_mjj
    #if(maxmj3_over_mjj<tmp_maxmj3_over_mjj) maxmj3_over_mjj = tmp_maxmj3_over_mjj;
    mystruct.runNumber=e.Run
    mystruct.eventNumber=e.Event    
    mystruct.averageIntPerXing=e.avIntPerXing
    #mystruct.n_pv=e.NVtx
    mystruct.n_tau=0
    mystruct.n_ph=e.NPhotons
    mystruct.n_el=0
    mystruct.n_mu=0
    mystruct.n_basemu=0
    mystruct.n_baseel=0
    #mystruct.n_jet=e.NJets
    mystruct.n_bjet=e.BTags
    mystruct.n_vx=int(e.NVtx)
    mystruct.trigger_met=1
    mystruct.trigger_lep=0

    tree_out.Fill()
    
    h1.Fill(1, weight)
    # apply MET cuts
    if not (e.MET>150.0):
        continue
    h1.Fill(3, weight)
    if not (e.MHTDefReb>120.0): #e.MHTDefReb*GeV # MHT includes the soft term. 
        continue
    h1.Fill(4, weight)
    if mystruct.n_jet!=2:
        continue
    h1.Fill(5, weight)
    # met soft
    if not (e.METsoft<20.0):
        continue
    h1.Fill(6, weight)

    # jet pT cuts
    if not (mystruct.jet_pt[0]>80.0):
        continue
    h1.Fill(7, weight)
    if not (mystruct.jet_pt[1]>50.0):
        continue
    h1.Fill(8, weight)

    # Deltaphi cuts
    if j1_met_dphi<1.0:
        continue
    h1.Fill(9, weight)
    if j2_met_dphi<1.0:
        continue
    h1.Fill(10, weight)
    # opposite hemi
    oppHemi = (mystruct.jet_eta[0] * mystruct.jet_eta[1])
    if oppHemi>0:
        continue
    h1.Fill(11, weight)

    # detajj cut
    if not (jj_deta>3.8):
        continue
    h1.Fill(12, weight)    

    # dphijj cut
    if not (jj_dphi < 1.8):
        continue
    h1.Fill(13, weight)
    # mjj cut
    if not (jj_mass >1000.0):
        continue
    h1.Fill(14, weight)

    if not IsLoose:
        # loose fjvt
        if e.JetFJVT[0]>0.5:
            continue
        if e.JetFJVT[1]>0.5:
            continue
    h1.Fill(15, weight)

    if not IsLoose:
        # very tight fjvt
        if e.MET<180.0:
            if e.JetFJVT[0]>0.2:
                continue
            if e.JetFJVT[1]>0.2:
                continue
        
    h1.Fill(16, weight)

fout.cd()
tree_out.Write()
fout.Write()
fout.Close()
f.Close()
print 'DONE'
