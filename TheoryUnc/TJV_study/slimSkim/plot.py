import ROOT

def Style():
    ROOT.gROOT.LoadMacro('/afs/desy.de/user/o/othrif/RootUtils/AtlasStyle.C')
    ROOT.gROOT.LoadMacro('/afs/desy.de/user/o/othrif/RootUtils/AtlasUtils.C')
    ROOT.SetAtlasStyle()

Style();
fout = ROOT.TFile.Open('myplt.root','RECREATE')
can = ROOT.TCanvas('stack', 'stack', 800, 500)

fileproc='W_EWK'
label="boson_Zll_Wlv_pt"
nhist=50
lowhist=100
highhist=1000
ratiolow=0.5
ratiohigh=1.5

common = " && jet_pt[0]>60e3 && jet_pt[1]>40e3 && n_jet>=2 && jet_eta[0]*jet_eta[1]<0 && jj_deta>2.5 && jj_dphi<2.4  && jj_mass>200e3 "
SR     = " (n_el+n_mu==0)"
CRee   = "( n_el==2 && n_mu==0 && abs(mll-91.2e3)<25e3 )"
CRmm   = "( n_el==0 && n_mu==2 && abs(mll-91.2e3)<25e3 )"
CRe   = "( n_el==1 && n_mu==0 )"
CRm   = "( n_el==0 && n_mu==1 )"

var1="boson_pt" #ee_pt
reg1=var1+"eeEWK"
leg1="Zll"
cuts1=CRee+common # && (n_mu==0 && n_nu==0)
var11="boson_pt"  #mumu_pt
reg11=var11+"mmEWK"
cuts11=CRmm+common#+common # && (n_mu==0 && n_nu==0)

#var2="nunu_pt"
#reg2=var2+"EWK"
#leg2="Zvv"
#cuts2="( n_nu==2 && n_jet>=2 )"#+common+SR # && (n_mu==0 && n_el==0)
#var2=var11
#reg2=reg11
#cuts2=cuts11
#leg2="Wlv"
var2="boson_pt"
reg2=var2+"eEWK"
cuts2=CRe+common
leg2="Wlv"
var22="boson_pt"
reg22=var22+"mEWK"
cuts22=CRm+common


f_Z_EWK = ROOT.TFile.Open('/nfs/dust/atlas/user/othrif/scratch/myPP/latest/processed/161219/Z_EWK.root')
tree_Z_EWK = f_Z_EWK.Get("nominal")
plt1 = ROOT.TH1F(var1+"_"+reg1,var1+"_"+reg1,nhist,lowhist,highhist)
tree_Z_EWK.Draw(var1+'*1.0e-3 >> '+var1+"_"+reg1,'w*36000.0*'+cuts1)
plt11 = ROOT.TH1F(var11+"_"+reg11,var11+"_"+reg11,nhist,lowhist,highhist)
tree_Z_EWK.Draw(var11+'*1.0e-3 >> '+var11+"_"+reg11,'w*36000.0*'+cuts11)
print "Nom1 channel: ", plt1.Integral()
plt1.Add(plt11)
print "Nom2 channel: ", plt11.Integral()
print "Total Nom channel: ", plt1.Integral()
plt1.Scale(1/plt1.Integral())
plt1.GetYaxis().SetTitle('Events')
plt1.GetXaxis().SetTitle('Boson pT [GeV]')
plt1.SetDirectory(fout)
plt1.SetMarkerSize(0.6)
fout.Write()

f_W_EWK = ROOT.TFile.Open('/nfs/dust/atlas/user/othrif/scratch/myPP/latest/processed/161219/W_EWK.root')
tree_W_EWK = f_W_EWK.Get("nominal")
plt2 = ROOT.TH1F(var2+"_"+reg2,var2+"_"+reg2,nhist,lowhist,highhist)
tree_W_EWK.Draw(var2+'*1.0e-3 >> '+var2+"_"+reg2,'w*36000.0*'+cuts2)
plt22 = ROOT.TH1F(var22+"_"+reg22,var22+"_"+reg22,nhist,lowhist,highhist)
tree_W_EWK.Draw(var22+'*1.0e-3 >> '+var22+"_"+reg22,'w*36000.0*'+cuts22)
print "Denom1 channel: ", plt2.Integral()
plt2.Add(plt22)
print "Denom2 channel: ", plt22.Integral()
print "Total Denom channel: ", plt2.Integral()
plt2.Scale(1/plt2.Integral())
plt2.SetDirectory(fout)
plt2.SetMarkerSize(0.6)
fout.Write()

# pads
pad1 = ROOT.TPad("pad1", "pad1", 0, 0.3, 1, 1.0);
pad1.SetBottomMargin(0); # Upper and lower plot are joined
#pad1.SetGridx();         # Vertical grid
pad1.Draw();             # Draw the upper pad: pad1
pad1.cd();               # pad1 becomes the current pad
pad1.SetLogy(1)


plt1.SetLineColor(1)
plt1.SetMarkerColor(1)
#plt1.DrawNormalized()
plt1.Draw()
plt2.SetLineColor(2)
plt2.SetMarkerColor(2)
#plt2.DrawNormalized("same")
plt2.Draw("same")

leg = ROOT.TLegend(0.8, 0.7, 0.98, 0.9)
leg.SetBorderSize(0)
leg.SetFillStyle (0)
leg.SetTextFont(42);
leg.SetTextSize(0.04);
leg.AddEntry(plt1,leg1)
leg.AddEntry(plt2,leg2)
leg.Draw()



can.cd();          # Go back to the main canvas before defining pad2
pad2 = ROOT.TPad("pad2", "pad2", 0, 0.03, 1, 0.3);
pad2.SetTopMargin(0);
pad2.SetBottomMargin(0.3);
pad2.SetGridy(); # vertical grid
pad2.Draw();
pad2.cd();       # pad2 becomes the current pad
pad2.SetLogy(0)

hratio = plt1.Clone()
hratio.Divide(plt2)
hratio.GetYaxis().SetTitle(leg1+'/'+leg2)
hratio.GetYaxis().SetRangeUser(ratiolow,ratiohigh)
hratio.GetYaxis().SetNdivisions(505);
hratio.GetYaxis().SetTitleSize(20);
hratio.GetYaxis().SetTitleFont(43);
hratio.GetYaxis().SetTitleOffset(1.55);
hratio.GetYaxis().SetLabelFont(43);
hratio.GetYaxis().SetLabelSize(15);
hratio.GetXaxis().SetTitleSize(20);
hratio.GetXaxis().SetTitleFont(43);
hratio.GetXaxis().SetTitleOffset(3.);
hratio.GetXaxis().SetLabelFont(43); # Absolute font size in pixel (precision 3)
hratio.GetXaxis().SetLabelSize(15);
hratio.Draw()
can.Update()
can.SaveAs(fileproc+"_"+label+".pdf")
can.WaitPrimitive()



