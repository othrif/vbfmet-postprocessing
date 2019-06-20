import ROOT
import pickle
import sys

def AddEvt(e,mapA,mapAVars,cut,r207=False):

    if cut not in mapA:
        mapA[cut]={}
        mapAVars[cut]={}
    if e.runNumber not in mapA[cut]:
        mapA[cut][e.runNumber]=[]
        mapAVars[cut][e.runNumber]={}
    if not r207:
        mapA[cut][e.runNumber] += [int(e.eventNumber)]
        #mapAVars[cut][e.runNumber][int(e.eventNumber)] = [e.j1_pt,e.j2_pt,e.lepmet_et,e.Inv_mass,e.jj_dphi]        
    else:
        mapA[cut][e.runNumber] += [int(e.eventNumber)]
        #mapAVars[cut][e.runNumber][int(e.eventNumber)] = [e.jet_pt[0],e.jet_pt[1],e.met_tst_et,e.jj_mass,e.jj_dphi]#,(e.trigger_met),e.n_mu, e.n_el, e.met_tst_et, e.met_tst_j1_dphi, e.met_tst_j2_dphi, e.passJetCleanTight,e.n_jet, e.jet_pt[0], e.jet_pt[1], e.jj_mass, e.jj_dphi, (e.jet_eta[0]*e.jet_eta[1]),e.jj_deta]

#physics_micro_NONE->Draw("el2_pt/1.0e3>>heln","mu_n==0 && el_n==2 && (el2_charge*el1_charge<0)  && lepmet_et>180.0e3 && metjet_CST>150e3 && jj_dphi<1.8 && jj_deta>3.5 && (elTrig>0 || muTrig>0)")

#fnew = ROOT.TFile.Open('microtuplesEvent/dataNomina.root')
fnew = ROOT.TFile.Open('/Users/schae/testarea/HInvNov/source/Plotting/v26Loose/data.root')
#fnew = ROOT.TFile.Open('/tmp/data.root')
fold = ROOT.TFile.Open('/tmp/merge_data.root')

tnew = fnew.Get('dataNominal')
#tnew = fnew.Get('MiniNtuple')
told = fold.Get('physics_micro_NONE')

doWCR=False
doZCR=True
doR21=1
missedEvt=[]
NewmissedEvt=[]
MYmatchedEvt=[]
MYmatchedEvtNew=[]
missingRuns=[]
runNew = {}
runOld = {}
runNewVars = {}
runOldVars = {}
nNewObs=0
nOldObs=0

if doR21>2 or doR21==0:
    u=0
    print 'Events: ',told.GetEntries()    
    for e in told:
        if u%10000==0:
            print 'Event: ',u,' ',(u/float(told.GetEntries()))
            sys.stdout.flush()
        u+=1    
        # synch cuts
        if e.Inv_mass<200.0e3:
            continue    
        if e.j1_pt<80.0e3:
            continue    
        if e.j2_pt<50.0e3:
            continue
        #if e.j3_pt>30.0e3:
        #    continue
        if e.jj_deta<3.5:
            continue;
        if e.jj_dphi>1.8:
            continue;
        if not doZCR:
            if e.met_et<150.0e3:
                continue;
        elif  doZCR:
            if e.lepmet_et<150.0e3:
                continue;
        if doZCR:
            if not ((e.el1_pt>30.0e3 and e.el_n>0) or (e.mu1_pt>30.0 and e.mu_n>0e3)):
                continue
        AddEvt(e,runOld,runOldVars,'all')
        if e.pass_JetCleaning_tight!=1:
            continue
        AddEvt(e,runOld,runOldVars,'jetcleaning')    
        # apply cutflow
        if doWCR:
            if e.muTrig!=1 and e.elTrig!=1:
                continue
            if not ((e.mu_n==1 and e.el_n==0) or (e.mu_n==0 and e.el_n==1)):
                continue
            if e.met_significance<4.0:
                continue
            if e.lepmet_et<180.0e3:
                continue
            if e.deltaPhi_j1_lepmet<1.0:
                continue
            if e.deltaPhi_j2_lepmet<1.0:
                continue
        elif doZCR:
            if e.muTrig!=1 and e.elTrig!=1:
                continue
            AddEvt(e,runOld,runOldVars,'lep_trig')
            if not ((e.mu_n==2 and e.mu1_pt>30.0e3 and e.mu2_pt>7.0e3) or (e.el_n==2 and e.el1_pt>30.0e3 and e.el2_pt>18.0e3)):
                continue
            AddEvt(e,runOld,runOldVars,'lep_pt')
            if not ((e.mu_n==2 and e.el_n==0 and e.mu1_charge*e.mu2_charge<0) or (e.mu_n==0 and e.el_n==2 and e.el1_charge*e.el2_charge<0)):
                continue
            AddEvt(e,runOld, runOldVars, 'lep_sel')
            #print e.Zll_m
            #if not (e.Zll_m>66.0e3 and e.Zll_m<116.0e3):
            #    continue
            if e.Zll_m<66.0e3:
                #print 'Fail low: ',e.Zll_m
                continue
            if e.Zll_m>116.0e3:
                #print 'Fail high: ',e.Zll_m
                continue
            #print 'mass z mass'
            AddEvt(e,runOld,runOldVars,'z_mass')
            if e.lepmet_et<180.0e3:
                continue
            AddEvt(e,runOld,runOldVars,'met_et')
            if e.metjet_CST<150.0e3:
                continue
            AddEvt(e,runOld,runOldVars,'cst')            
            if e.deltaPhi_j1_lepmet<1.0:
                continue
            if e.deltaPhi_j2_lepmet<1.0:
                continue
            AddEvt(e,runOld,runOldVars,'met_jet_dphi')
        else:
            if e.MET_trig!=1:
                continue        
            AddEvt(e,runOld,runOldVars,'met_trig')
            if e.mu_n!=0:
                continue
            AddEvt(e,runOld,runOldVars,'n_mu')
            if e.el_n!=0:
                continue;
            AddEvt(e,runOld,runOldVars,'n_el')
            if e.met_et<180.0e3:
                continue
            AddEvt(e,runOld,runOldVars,'met_et')
            if e.metjet_CST<150.0e3:
                continue
            AddEvt(e,runOld,runOldVars,'cst')
            if e.deltaPhi_j1_met<1.0:
                continue
            if e.deltaPhi_j2_met<1.0:
                continue
            AddEvt(e,runOld,runOldVars,'met_jet_dphi')
        if e.j1_pt<80.0e3:
            continue
        AddEvt(e,runOld,runOldVars,'j1_pt')
        if e.j2_pt<50.0e3:
            continue
        AddEvt(e,runOld,runOldVars,'j2_pt')
        #if e.jet_n!=2:
        #    continue
        AddEvt(e,runOld,runOldVars,'n_jet')
        #if e.j3_pt>25.0e3:
        #    continue
        if e.Inv_mass<1000.0e3:
            continue
        AddEvt(e, runOld, runOldVars, 'jj_mass')
        if (e.jj_dphi>1.8):
            continue
        AddEvt(e, runOld, runOldVars, 'jj_dphi')
        if (e.j1_eta*e.j2_eta)>0.0:
            continue
        AddEvt(e, runOld, runOldVars, 'hemi')
        if e.jj_deta<4.8:
            continue;
        AddEvt(e, runOld, runOldVars, 'jj_deta')
        nOldObs+=1

    #v207=[runOld,runOldVars]
    v207=[runOld,{}]
    pickle.dump( v207, open( "r207AllJets.p", "wb" ) )

v1=ROOT.TLorentzVector()
v2=ROOT.TLorentzVector()
if doR21==1 or doR21>2:
    u=0
    print 'Events: ',tnew.GetEntries()
    for e in tnew:
        if u%10000==0:
            print 'Event: ',u,' ',(u/4417630.0)
            sys.stdout.flush()
        u+=1
        # synch cuts
        if e.jj_mass<200.0e3:
            continue
        if e.jj_dphi>1.8:
            continue
        if e.jj_deta<3.5:
            continue;
        if not doZCR:
            if e.met_tst_et<150.0e3:
                continue;
        elif doZCR:
            if e.met_tst_nolep_et<100.0e3:
                continue;
        if e.jet_pt[0]<90.0e3:
            continue    
        if e.jet_pt[1]<50.0e3:
            continue
        if doZCR:
            if not ((e.n_el>0 and e.el_pt[0]>30.0e3) or (e.n_mu>0 and e.mu_pt[0]>30.0e3)):
                continue
        AddEvt(e,runNew,runNewVars,'all',True)
        if e.passJetCleanTight!=1:
            continue
        AddEvt(e,runNew,runNewVars,'jetcleaning',True)
        
        #if not (e.runNumber in runOld):
        #    continue
        #if not (int(e.eventNumber) in runOld[e.runNumber]):
        #    continue;
        # apply cutflow
        if doWCR:
            if e.trigger_lep!=1:
                continue
            if not ((e.n_mu==1 and e.n_el==0) or (e.n_mu==0 and e.n_el==1)):
                continue
            if e.met_significance<4.0:
                continue        
            if e.met_tst_nolep_et<180.0e3:
                continue        
            if e.met_tst_nolep_j1_dphi<1.0:
                continue
            if e.met_tst_nolep_j2_dphi<1.0:
                continue
        elif doZCR:
            if not (e.trigger_lep & 0x1 == 1):
                continue
            AddEvt(e,runNew,runNewVars,'lep_trig',True)
            #if not ((e.n_mu==2 and e.mu_pt[0]>30.0e3 and e.mu_pt[1]>7.0e3) or (e.n_el==2 and e.el_pt[0]>30.0e3 and e.el_pt[1]>7.0e3)):
            #if not ((e.n_mu==2 and e.mu_pt[0]>30.0e3 and e.mu_pt[1]>7.0e3)):
            if not ((e.n_el==2 and e.el_pt[0]>30.0e3 and e.el_pt[1]>18.0e3)):
                continue
            AddEvt(e,runNew,runNewVars,'lep_pt')
            if not ((e.n_mu==2 and e.n_el==0 and e.mu_charge[0]*e.mu_charge[1]<0) or (e.n_mu==0 and e.n_el==2 and e.el_charge[0]*e.el_charge[1]<0)):
                continue
            AddEvt(e,runNew,runNewVars,'lep_sel')
            if e.n_mu==2 and (abs(e.mu_eta[0])>2.5 or abs(e.mu_eta[1])>2.5):
                continue
            if e.n_el==2 and ((abs(e.el_eta[0])>1.37 and abs(e.el_eta[0])<1.52) or (abs(e.el_eta[1])>1.37 and abs(e.el_eta[1])<1.52)):
                continue
            if e.n_mu==2:
                v1.SetPtEtaPhiM(e.mu_pt[0],e.mu_eta[0],e.mu_phi[0],106.0)
                v2.SetPtEtaPhiM(e.mu_pt[1],e.mu_eta[1],e.mu_phi[1],106.0)
            elif e.n_el==2:
                v1.SetPtEtaPhiM(e.el_pt[0],e.el_eta[0],e.el_phi[0],0.511)
                v2.SetPtEtaPhiM(e.el_pt[1],e.el_eta[1],e.el_phi[1],0.511)
            Zll_mb=(v1+v2).M()
            if Zll_mb<66.0e3:
                continue
            if  Zll_mb>116.0e3:
                continue
            AddEvt(e,runNew, runNewVars, 'z_mass')
            if e.met_tst_nolep_et<180.0e3:
                continue
            AddEvt(e,runNew,runNewVars,'met_et')
            if e.met_cst_jet<150.0e3:
                continue
            AddEvt(e,runNew,runNewVars,'cst')            
            if e.met_tst_nolep_j1_dphi<1.0:
                continue
            if e.met_tst_nolep_j2_dphi<1.0:
                continue
            AddEvt(e,runNew,runNewVars,'met_jet_dphi')
        else:
            #acz=''
            #if e.trigger_met!=1:
            #    continue
            if e.trigger_met<0.5 and e.trigger_met_encoded==0:
                continue
            AddEvt(e,runNew,runNewVars,'met_trig',True)        
            #if e.n_mu!=0:
            #    continue
            AddEvt(e,runNew,runNewVars,'n_mu',True)
            #if e.n_el!=0:
            #if e.n_el>0 and e.el_pt[0]>18.0e3:
            #    continue;
            AddEvt(e,runNew,runNewVars,'n_el',True)
            if e.met_tst_et<100.0e3: 
                continue
            AddEvt(e,runNew,runNewVars,'met_et',True)
            #if e.met_cst_jet<135.0e3:
            #    continue        
            AddEvt(e,runNew,runNewVars,'cst',True)
            if e.met_tst_j1_dphi<1.0:
                continue
            if e.met_tst_j2_dphi<1.0:
                continue
            AddEvt(e,runNew,runNewVars,'met_jet_dphi',True)
        if e.jet_pt[0]<80.0e3: # 80
            continue
        AddEvt(e,runNew,runNewVars,'j1_pt',True)
        if e.jet_pt[1]<50.0e3: # 50
            continue
        AddEvt(e,runNew,runNewVars,'j2_pt',True)
        #if e.n_jet==3 and e.jet_pt[2]>35.0e3: # 50
        #    continue
        if e.n_jet!=2:
            continue
        AddEvt(e,runNew,runNewVars,'n_jet',True)
        if e.jj_mass<1000.0e3:
            continue
        AddEvt(e,runNew,runNewVars,'jj_mass',True)
        if e.jj_dphi>1.8:
            continue
        AddEvt(e,runNew,runNewVars,'jj_dphi',True)
        if e.jet_eta[0]*e.jet_eta[1]>0.0:
            continue
        AddEvt(e,runNew,runNewVars,'hemi',True)
        if e.jj_deta<4.8:
            continue;
        AddEvt(e,runNew,runNewVars,'jj_deta',True)
    
        #runNewVars[e.runNumber][int(e.eventNumber)] = [e.jet_pt[0],e.jet_pt[1],e.met_tst_et,e.jj_mass,e.jj_dphi,(e.trigger_HLT_xe110_mht_L1XE50<0.5 and e.trigger_HLT_xe90_mht_L1XE50<0.5 and e.trigger_HLT_xe100_mht_L1XE50<0.5),e.n_mu, e.n_el, e.met_tst_et, e.met_tst_j1_dphi, e.met_tst_j2_dphi, e.passJetCleanTight,e.n_jet, e.jet_pt[0], e.jet_pt[1], e.jj_mass, e.jj_dphi, (e.jet_eta[0]*e.jet_eta[1]),e.jj_deta]
    #v21=[runNew,runNewVars]
    v21=[runNew,{}]
    pickle.dump( v21, open( "r21Zee3018.p", "wb" ) )

print 'New: ',len(runNew)
print 'old: ',len(runOld)

print 'Observed Old: ',nOldObs,' new: ',nNewObs

matched=0
unmatched=0
matchedEvt=[]
unmatchedEvt=[]
for run,events in runOld.iteritems():    
    print run
    if run in runNew:
        print 'run found!'
        for e in events:
            if e in runNew[run]:
                matched+=1;
                matchedEvt+=[{run:e}]
                MYmatchedEvt+=[runOldVars[run][e]]
                MYmatchedEvtNew+=[runNewVars[run][e]]
            else:
                unmatched+=1;
                unmatchedEvt+=[{run:e}]
                print 'unmatched:',runOldVars[run][e]
                missedEvt+=[runOldVars[run][e]]
    else:
        missingRuns+=[run]


for run,events in runNew.iteritems():           
    if run in runOld:
        for e in events:
            if e in runOld[run]:
                continue;
            else:
                NewmissedEvt+=[runNewVars[run][e]]
    else:
        print 'miss run: ',run

        
print 'matched: ',matched
print 'unmatched: ',unmatched

print 'matched:',matchedEvt
print 'unmatched:',unmatchedEvt
print 'missingRuns: ',missingRuns


fout = None
if doWCR:
    fout = ROOT.TFile.Open('foutWCR.root','RECREATE')
else:
    fout = ROOT.TFile.Open('foutSRAll2_newLooseMet.root','RECREATE')
    
hmet = ROOT.TH1F('met','met',500,0.0,500.0)
hmet.SetDirectory(fout)
hj0 = ROOT.TH1F('j0','j0',500,0.0,500.0)
hj0.SetDirectory(fout)
hj1 = ROOT.TH1F('j1','j1',500,0.0,500.0)
hj1.SetDirectory(fout)
hmjj = ROOT.TH1F('mjj','mjj',500,0.0,5000.0)
hmjj.SetDirectory(fout)
hdphijj = ROOT.TH1F('dphijj','dphijj',32,0.0,3.2)
hdphijj.SetDirectory(fout)

#matched
hMatchmet = ROOT.TH1F('Matchmet','Matchmet',500,0.0,500.0)
hMatchmet.SetDirectory(fout)
hMatchj0 = ROOT.TH1F('Matchj0','Matchj0',500,0.0,500.0)
hMatchj0.SetDirectory(fout)
hMatchj1 = ROOT.TH1F('Matchj1','Matchj1',500,0.0,500.0)
hMatchj1.SetDirectory(fout)
hMatchmjj = ROOT.TH1F('Matchmjj','Matchmjj',500,0.0,5000.0)
hMatchmjj.SetDirectory(fout)
hMatchdphijj = ROOT.TH1F('Matchdphijj','Matchdphijj',32,0.0,3.2)
hMatchdphijj.SetDirectory(fout)


hMatchNewmet = ROOT.TH1F('MatchNewmet','MatchNewmet',500,0.0,500.0)
hMatchNewmet.SetDirectory(fout)
hMatchNewj0 = ROOT.TH1F('MatchNewj0','MatchNewj0',500,0.0,500.0)
hMatchNewj0.SetDirectory(fout)
hMatchNewj1 = ROOT.TH1F('MatchNewj1','MatchNewj1',500,0.0,500.0)
hMatchNewj1.SetDirectory(fout)
hMatchNewmjj = ROOT.TH1F('MatchNewmjj','MatchNewmjj',500,0.0,5000.0)
hMatchNewmjj.SetDirectory(fout)
hMatchNewdphijj = ROOT.TH1F('MatchNewdphijj','MatchNewdphijj',32,0.0,3.2)
hMatchNewdphijj.SetDirectory(fout)

#not matched but in the new ntuple
hNewMissmet = ROOT.TH1F('NewMissmet','NewMissmet',500,0.0,500.0)
hNewMissmet.SetDirectory(fout)
hNewMissj0 = ROOT.TH1F('NewMissj0','NewMissj0',500,0.0,500.0)
hNewMissj0.SetDirectory(fout)
hNewMissj1 = ROOT.TH1F('NewMissj1','NewMissj1',500,0.0,500.0)
hNewMissj1.SetDirectory(fout)
hNewMissmjj = ROOT.TH1F('NewMissmjj','NewMissmjj',500,0.0,5000.0)
hNewMissmjj.SetDirectory(fout)
hNewMissdphijj = ROOT.TH1F('NewMissdphijj','NewMissdphijj',32,0.0,3.2)
hNewMissdphijj.SetDirectory(fout)

# differences
hDiffmet = ROOT.TH1F('Diffmet','Diffmet',1000,-500.0,500.0)
hDiffmet.SetDirectory(fout)
hDiffj0 = ROOT.TH1F('Diffj0','Diffj0',1000,-500.0,500.0)
hDiffj0.SetDirectory(fout)
hDiffj1 = ROOT.TH1F('Diffj1','Diffj1',1000,-500.0,500.0)
hDiffj1.SetDirectory(fout)
hDiffmjj = ROOT.TH1F('Diffmjj','Diffmjj',1000,-5000.0,5000.0)
hDiffmjj.SetDirectory(fout)
hDiffdphijj = ROOT.TH1F('Diffdphijj','Diffdphijj',64,-3.2,3.2)
hDiffdphijj.SetDirectory(fout)

for e in missedEvt:
    hj0.Fill(e[0]/1.0e3)
    hj1.Fill(e[1]/1.0e3)
    hmet.Fill(e[2]/1.0e3)
    hmjj.Fill(e[3]/1.0e3)
    hdphijj.Fill(e[4])
for e in MYmatchedEvt:
    hMatchj0.Fill(e[0]/1.0e3)
    hMatchj1.Fill(e[1]/1.0e3)
    hMatchmet.Fill(e[2]/1.0e3)
    hMatchmjj.Fill(e[3]/1.0e3)
    hMatchdphijj.Fill(e[4])
for e in MYmatchedEvtNew:
    hMatchNewj0.Fill(e[0]/1.0e3)
    hMatchNewj1.Fill(e[1]/1.0e3)
    hMatchNewmet.Fill(e[2]/1.0e3)
    hMatchNewmjj.Fill(e[3]/1.0e3)
    hMatchNewdphijj.Fill(e[4])    
for e in NewmissedEvt:
    hNewMissj0.Fill(e[0]/1.0e3)
    hNewMissj1.Fill(e[1]/1.0e3)
    hNewMissmet.Fill(e[2]/1.0e3)
    hNewMissmjj.Fill(e[3]/1.0e3)
    hNewMissdphijj.Fill(e[4])      

for e in range(0,len(MYmatchedEvt)):
    hDiffj0.Fill((MYmatchedEvt[e][0]-MYmatchedEvtNew[e][0])/1.0e3)
    hDiffj1.Fill((MYmatchedEvt[e][1]-MYmatchedEvtNew[e][1])/1.0e3)
    hDiffmet.Fill((MYmatchedEvt[e][2]-MYmatchedEvtNew[e][2])/1.0e3)
    hDiffmjj.Fill((MYmatchedEvt[e][3]-MYmatchedEvtNew[e][3])/1.0e3)
    hDiffdphijj.Fill((MYmatchedEvt[e][4]-MYmatchedEvtNew[e][4]))

fout.Write()
fout.Close()

print ''
for run,events in runOld.iteritems():
    for e in events:
        print run,' ',e 

# run cutflow
labs = ['all','trig','n_mu','n_el','met_tst_et','met_tst_j1_dphi','met_tst_j2_dphi','passJetCleanTight',
            'n_jet','j1','j2','mjj','dphijj','hemi','deta']
cutflow={}
for l in labs:
    cutflow[l]=0
#for e in MYmatchedEvtNew:
for e in range(0,len(MYmatchedEvtNew)):
    cutflow['all']+=1
    if MYmatchedEvtNew[e][5]:
        continue
    cutflow['trig']+=1
    if MYmatchedEvtNew[e][6]!=0:
        continue
    cutflow['n_mu']+=1
    if MYmatchedEvtNew[e][7]!=0:
        continue;
    cutflow['n_el']+=1    
    if MYmatchedEvtNew[e][8]<180.0e3: 
        continue
    cutflow['met_tst_et']+=1 
    if MYmatchedEvtNew[e][9]<1.0:
        continue
    cutflow['met_tst_j1_dphi']+=1
    if MYmatchedEvtNew[e][10]<1.0:
        continue
    cutflow['met_tst_j2_dphi']+=1
    if MYmatchedEvtNew[e][11]!=1:
        continue
    cutflow['passJetCleanTight']+=1
    if MYmatchedEvtNew[e][12]!=2:
        continue
    cutflow['n_jet']+=1
    if MYmatchedEvtNew[e][13]<75.0e3: # 80
        continue
    cutflow['j1']+=1
    if MYmatchedEvtNew[e][14]<40.0e3: # 50
        continue
    cutflow['j2']+=1
    if MYmatchedEvtNew[e][15]<1000.0e3:
        continue
    cutflow['mjj']+=1
    if MYmatchedEvtNew[e][16]>1.8:
        continue
    cutflow['dphijj']+=1
    if MYmatchedEvtNew[e][17]>0.0:
        continue
    cutflow['hemi']+=1
    if MYmatchedEvtNew[e][18]<4.8:
        continue;
    cutflow['deta']+=1

print 'cutflow:'
for l in labs:
    print l,' ',cutflow[l]
