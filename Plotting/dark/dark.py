import ROOT
import math

def GetUpper(h,fcolor):

    h.SetFillColor(fcolor)
    h.SetLineColor(fcolor)    
    h.SetMarkerColor(fcolor)    
    for i in range(0,h.GetNbinsX()+1):
        ymax=0
        for j in range(0,h.GetNbinsY()+1):        
            if h.GetBinContent(i,j)>0:
                ymax = j
        for j in range(0,ymax):
            h.SetBinContent(i,j,0.0)

def getVals(Nc, eU, eD, qU, qD):
    R0=Nc*(eU**2+eD**2)
    R1=Nc*(qU**2+qD**2)*3.0
    R=Nc*(eU*qU+eD*qD)*3.0

    alpha = 1.0/137.0
    rgg=0.1
    BR_inv = 0.13
    BR_SM_gg = 0.00228
    rgdgd = 1.0 # not needed
    #N = BR_SM_gg/(1.0+rgdgd*BR_SM_gg)
    alpha_dark = (R0/R1)*alpha*math.sqrt(BR_inv/((1-BR_inv)*BR_SM_gg*rgg))
    k=BR_SM_gg*(1.0+rgg)/(1+math.sqrt(rgg))**2
    alpha_dark2 = alpha*math.sqrt((BR_SM_gg-k)/(k*BR_SM_gg*rgg*(R1/R0)**2))
    k=BR_SM_gg*(1.0-rgg)/(1+math.sqrt(rgg))**2
    alpha_dark3 = alpha*math.sqrt((BR_SM_gg-k)/(k*BR_SM_gg*rgg*(R1/R0)**2))
    print 'alpha_dark: %0.3f rgg limit: %0.3f rgg limitdown: %0.3f' %(alpha_dark,alpha_dark2,alpha_dark3)

    
    rgdgd = rgg *(R1/R0)**2*(alpha_dark/alpha)**2
    BR_ggd = 2.0*rgg*(R/R0)**2 *(alpha_dark/alpha)*(BR_SM_gg/(1+BR_SM_gg*rgdgd))
    print 'BR_ggd: %0.3f' %(BR_ggd)
    print ''

def plot(mes_type,Nc, eU, eD, qU, qD):

    hlim = ROOT.TH2F('hlim','hlim',500, 0.0,1.0 , 500,0.0,0.02)
    hlim.SetStats(0)
    rand =ROOT.TRandom3();
    rand.SetSeed(5);
    
    # scan values of rgg
    for i in range(0,50000):#50000
        g=rand.Rndm() # value of 0-1.0
        rggInput=0.1*g
        allowedPoints = isExcl(Nc, eU, eD, qU, qD, rand, rggInput = rggInput)
        for p in allowedPoints:
            hlim.Fill(p[0],p[1])

    can = ROOT.TCanvas('table', 'table', 600, 850)
    can.Draw()
    can.cd()
    hlim.GetXaxis().SetTitle('#bar{#alpha}')
    #hlim.GetXaxis().SetTitle('#bar{#alpha} / <q*e>')    
    #hlim.GetXaxis().SetTitle('#bar{#alpha} / R ')
    hlim.GetYaxis().SetTitle('Br[h#rightarrow#gamma#gamma_{d}]')
    hlim.Draw('colz')

    text = ROOT.TLatex(0.3, 0.7, mes_type)
    text.SetNDC()
    text.SetTextSize(0.055)
    text.SetTextAlign(11)
    text.SetTextColor(ROOT.kBlack)
    text.Draw()
    can.Update()
    #can.WaitPrimitive()
    #raw_input('')
    return hlim.Clone()
    
def isExcl(Nc, eU, eD, qU, qD, rand, rggInput = 0.1):
    R0=Nc*(eU**2+eD**2)
    R1=Nc*(qU**2+qD**2)*3.0 # 3 is for the number of messengers
    R=Nc*(eU*qU+eD*qD)*3.0 # 3 is for the number of messengers
    avgDarkChr = (abs(qU)+abs(qD))/2.0
    if qU==0.0:
        avgDarkChr=qD
    if qD==0.0:
        avgDarkChr=qU
    avgEMChr = (abs(eU)+abs(eD))/2.0
    if eU==0.0:
        avgEMChr=eD
    if eD==0.0:
        avgEMChr=eU
    avgChr = avgEMChr*avgDarkChr
    avgChr = abs(R)
    avgChr=1.0
    alpha = 1.0/137.0
    rgg=rggInput
    BR_inv = 0.13
    BR_SM_gg = 0.00228
    #N = BR_SM_gg/(1.0+rgdgd*BR_SM_gg)
    alpha_dark_inv = (R0/R1)*alpha*math.sqrt(BR_inv/((1-BR_inv)*BR_SM_gg*rgg))

    # computes the limit using the BR(h->gg).
    SM_gg_limit_up=0.09
    k=BR_SM_gg*(1.0+SM_gg_limit_up)/(1+math.sqrt(rgg))**2
    alpha_dark_ggUP=0.0
    if BR_SM_gg-k>0.0:
        alpha_dark_ggUP = alpha*math.sqrt(abs(BR_SM_gg-k)/(k*BR_SM_gg*rgg*(R1/R0)**2))
    
    SM_gg_limit_dw=0.17
    k=BR_SM_gg*(1.0-SM_gg_limit_dw)/(1+math.sqrt(rgg))**2
    alpha_dark_ggDOWN=0.0
    if BR_SM_gg-k>0.0:
        alpha_dark_ggDOWN = alpha*math.sqrt(abs(BR_SM_gg-k)/(k*BR_SM_gg*rgg*(R1/R0)**2))

    # make sure that higgs to invisible limits are higher than the H->gg limits
    alpha_dark_ggMIN = min(alpha_dark_ggUP,alpha_dark_ggDOWN)
    alpha_dark_ggMAX = max(alpha_dark_ggUP,alpha_dark_ggDOWN)    
    if alpha_dark_inv<alpha_dark_ggMIN:
        return [] # everything is excluded
    alpha_dark_ggUp = min(alpha_dark_ggMAX,alpha_dark_inv)
    #return [alpha_dark_ggMIN,alpha_dark_ggUp] # allowable range

    # scan values of alpha_dark
    allowablePoints = []
    for i in range(0,1000):
        g=rand.Rndm()
        alpha_dark = g*(alpha_dark_ggUp-alpha_dark_ggMIN)+alpha_dark_ggMIN
        rgdgd = rgg *(R1/R0)**2*(alpha_dark/alpha)**2
        N=(BR_SM_gg/(1+BR_SM_gg*rgdgd))
        BR_ggd = 2.0*rgg*(R/R0)**2 *(alpha_dark/alpha)*N
        allowablePoints+=[[alpha_dark/avgChr, BR_ggd]]
    return allowablePoints

# up type
Nc=3.0 #number of colors
eU=2.0/3.0
eD=0.0
qU=1.0
qD=0.0
print 'up type'
getVals(Nc, eU, eD, qU, qD)
uphlim = plot('Up Type Messenger',Nc, eU, eD, qU, qD)
uphlim.SetName('up')
# down type
Nc=3.0 #number of colors
eU=0.0
eD=-1.0/3.0
qU=0.0
qD=1.0
print 'down type'
getVals(Nc, eU, eD, qU, qD)
dwhlim = plot('Down Type Messenger',Nc, eU, eD, qU, qD)
dwhlim.SetName('dwup')
#all
Nc=3.0
eU=2.0/3.0
eD=-1.0/3.0
qU=1.0
qD=1.0
print 'up+down type'
getVals(Nc, eU, eD, qU, qD)
updwlim = plot('Up+Down Type Messenger',Nc, eU, eD, qU, qD)
updwlim.SetName('dwup')

#leptonic
Nc=1.0
eU=0
eD=-1.0
qU=1.0
qD=1.0
print 'leptonic type'
getVals(Nc, eU, eD, qU, qD)
leplim = plot('Leptonic Messenger',Nc, eU, eD, qU, qD)
leplim.SetName('lep')

print 'Ending'
R0=Nc*(eU**2+eD**2)
R1=Nc*(qU**2+qD**2)*3.0
R=Nc*(eU*qU+eD*qD)*3.0

alpha = 1.0/137.0
rgg=1.0
BR_inv = 0.13
BR_SM_gg = 0.00228
rgdgd = 1.0 # not needed


alpha_dark = (R0/R1)*alpha*math.sqrt(BR_inv/((1-BR_inv)*BR_SM_gg*rgg))

print 'alpha_dark: %0.3f' %(alpha_dark)

rgdgd = rgg *(R1/R0)**2*(alpha_dark/alpha)**2
BR_ggd = 2.0*rgg*(R/R0)**2 *(alpha_dark/alpha)*(BR_SM_gg/(1+BR_SM_gg*rgdgd))
print 'BR_ggd: %0.3f' %(BR_ggd)

#generic q=e=1 Nc=3 [number of colors] model
Nc=3.0
eU=1.0
eD=0.0
qU=1.0
qD=0.0
print 'Generic type'
getVals(Nc, eU, eD, qU, qD)
genlim = plot('Generic Messenger',Nc, eU, eD, qU, qD)
genlim.SetName('gen')

#generic e=1 q=10 Nc=3 [number of colors] model, varying dark charge UP
Nc=3.0
eU=1.0
eD=0.0
qU=10.0
qD=0.0
print 'charge 10 type'
getVals(Nc, eU, eD, qU, qD)
char10lim = plot('dark charge 10 Messenger',Nc, eU, eD, qU, qD)
char10lim.SetName('dchr10')

#generic q=0.5 e=1 Nc=3 [number of colors] model, varying dark charge DOWN
Nc=3.0
eU=1.0
eD=0.0
qU=0.5
qD=0.0
print 'charge 0.5 type'
getVals(Nc, eU, eD, qU, qD)
char05lim = plot('dark charge 0.5 Messenger',Nc, eU, eD, qU, qD)
char05lim.SetName('dchr05')

#generic q=1 e=0.5 Nc=3 [number of colors] model, varying EM charge Dw
Nc=3.0
eU=0.5
eD=0.0
qU=1.0
qD=0.0
print 'charge 0.5 type'
getVals(Nc, eU, eD, qU, qD)
emchar05lim = plot('EM 0.5 Messenger',Nc, eU, eD, qU, qD)
emchar05lim.SetName('emchr05')

#generic q=1 e=2 Nc=3 [number of colors] model, varying EM charge Up
Nc=3.0
eU=2.0
eD=0.0
qU=1.0
qD=0.0
print 'charge 2 type'
getVals(Nc, eU, eD, qU, qD)
emchar2lim = plot('EM 2 Messenger',Nc, eU, eD, qU, qD)
emchar2lim.SetName('emchr2')


GetUpper(genlim,1)
GetUpper(leplim,2)
GetUpper(uphlim,3)
GetUpper(dwhlim,4)
GetUpper(updwlim,5)
GetUpper(char05lim,ROOT.kOrange)
GetUpper(char10lim,ROOT.kMagenta)
GetUpper(emchar05lim,ROOT.kCyan)
GetUpper(emchar2lim,ROOT.kCyan+2)


can = ROOT.TCanvas('table', 'table', 600, 850)
can.Draw()
can.cd()
genlim.Draw()
dopt='BOX same'
genlim.Draw(dopt)
leplim.Draw(dopt)
uphlim.Draw(dopt)
dwhlim.Draw(dopt)
updwlim.Draw(dopt)
#char10lim.Draw(dopt)
#char05lim.Draw(dopt)
#emchar05lim.Draw(dopt)
#emchar2lim.Draw(dopt)

leg=ROOT.TLegend(0.6,0.6,0.8,0.8)
leg.SetFillColor(0)
leg.SetBorderSize(0)
leg.AddEntry(genlim,'Generic e=q=1 Mess.')
leg.AddEntry(leplim,'Leptonic Mess.')
leg.AddEntry(uphlim,'Up Type Mess.')
leg.AddEntry(dwhlim,'Down Type Mess.')
leg.AddEntry(updwlim,'Up+Down Type Mess.')
#leg.AddEntry(char10lim,'Generic q=10 Mess.')
#leg.AddEntry(char05lim,'Generic q=0.5 e=1 Mess.')
#leg.AddEntry(emchar05lim,'Generic q=1 e=0.5 Mess.')
#leg.AddEntry(emchar2lim,'Generic q=1 e=2 Mess.')
leg.Draw()

can.Update()
can.WaitPrimitive()
raw_input('')
