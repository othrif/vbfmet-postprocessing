
// C/C++
#include <cstdlib>

// ROOT
#include "TH1.h"
#include "TH2.h"
#include "TH3.h"

// Local
#include "HInvPlot/UtilCore.h"
#include "HInvPlot/IExecAlg.h"

using namespace std;

//-----------------------------------------------------------------------------
Msl::IExecAlg::IExecAlg():
  fDebug     (false),
  fPrint     (false),
  fUseName   (true),
  fPassStatus(false),
  fPassWeight(0.0)
{
}

//-----------------------------------------------------------------------------
void Msl::IExecAlg::DoConf(const Registry &reg)
{
  reg.Get(GetType() + "::Debug",   fDebug);
  reg.Get(GetType() + "::Print",   fPrint);
  reg.Get(GetType() + "::UseName", fUseName);

  if(fDebug) {
    log() << "DoConf - called by base class... print Registry: " << endl;
    reg.Print();
  }
}

//-----------------------------------------------------------------------------
void Msl::IExecAlg::DoSave(TDirectory *idir)
{
  //
  // Save histograms
  //
  TDirectory *dir = idir;
  
  if(fUseName) {
    dir = Msl::GetDir(idir, fName);
  }

  if(!idir) {
    return;
  }

  for(HistMap::iterator hit = fHists.begin(); hit != fHists.end(); ++hit) {
    TH1 *h = hit->second;

    if(h) {
      h->SetDirectory(dir);
    }
  }
  for(HistMap2D::iterator hit = fHists2D.begin(); hit != fHists2D.end(); ++hit) {
    TH2 *h = hit->second;

    if(h) {
      h->SetDirectory(dir);
    }
  }
  for(HistMap3D::iterator hit = fHists3D.begin(); hit != fHists3D.end(); ++hit) {
    TH3 *h = hit->second;

    if(h) {
      h->SetDirectory(dir);
    }
  }
}

//-----------------------------------------------------------------------------
TH1* Msl::IExecAlg::GetTH1(const std::string &name, int nbin,  float arr[])
{
  //
  // Create TH1 histogram and set directory
  //
  
  HistMap::iterator hit = fHists.find(name);
  if(hit != fHists.end()) {
    return hit->second;
  }
  
  TH1 *h = new TH1D(name.c_str(), name.c_str(), nbin, arr);

  if(h) {
    if(!fHists.insert(HistMap::value_type(name, h)).second) {
      log() << "GetTH1 - ignore duplicate histogram: " << name << endl;
    }

    h->SetDirectory(0);
    h->Sumw2();
  }

  return h;
}

//-----------------------------------------------------------------------------
TH1* Msl::IExecAlg::GetTH1(const std::string &name, int nbin, double xmin, double xmax)
{
  //
  // Create TH1 histogram and set directory
  //
  
  HistMap::iterator hit = fHists.find(name);
  if(hit != fHists.end()) {
    return hit->second;
  }
  
  TH1 *h = new TH1D(name.c_str(), name.c_str(), nbin, xmin, xmax);

  if(h) {
    if(!fHists.insert(HistMap::value_type(name, h)).second) {
      log() << "GetTH1 - ignore duplicate histogram: " << name << endl;
    }

    h->SetDirectory(0);
    h->Sumw2();
  }

  return h;
}

//-----------------------------------------------------------------------------
TH2* Msl::IExecAlg::GetTH2(const std::string &name, int xnbin, double xmin, double xmax, int ynbin, double ymin, double ymax)
{
  //
  // Create TH2 histogram and set directory
  //
  
  HistMap2D::iterator hit = fHists2D.find(name);
  if(hit != fHists2D.end()) {
    return hit->second;
  }
  
  TH2 *h = new TH2D(name.c_str(), name.c_str(), xnbin, xmin, xmax, ynbin, ymin, ymax);

  if(h) {
    if(!fHists2D.insert(HistMap2D::value_type(name, h)).second) {
      log() << "GetTH2 - ignore duplicate histogram: " << name << endl;
    }

    h->SetDirectory(0);
    h->Sumw2();
  }

  return h;
}

//-----------------------------------------------------------------------------
TH2* Msl::IExecAlg::GetTH2(const std::string &name, int nbinx,  float xarr[], int nbiny,  float yarr[])
{
  //
  // Create TH2 histogram and set directory
  //
  
  HistMap2D::iterator hit = fHists2D.find(name);
  if(hit != fHists2D.end()) {
    return hit->second;
  }
  
  TH2 *h = new TH2D(name.c_str(), name.c_str(), nbinx, xarr, nbiny, yarr);

  if(h) {
    if(!fHists2D.insert(HistMap2D::value_type(name, h)).second) {
      log() << "GetTH2 - ignore duplicate histogram: " << name << endl;
    }

    h->SetDirectory(0);
    h->Sumw2();
  }

  return h;
}

//-----------------------------------------------------------------------------
TH3* Msl::IExecAlg::GetTH3(const std::string &name, int xnbin, double xmin, double xmax, int ynbin, double ymin, double ymax,
			   int znbin, double zmin, double zmax)
{
  //
  // Create TH3 histogram and set directory
  //
  
  HistMap3D::iterator hit = fHists3D.find(name);
  if(hit != fHists3D.end()) {
    return hit->second;
  }
  
  TH3 *h = new TH3D(name.c_str(), name.c_str(), xnbin, xmin, xmax, ynbin, ymin, ymax, znbin, zmin, zmax);

  if(h) {
    if(!fHists3D.insert(HistMap3D::value_type(name, h)).second) {
      log() << "GetTH3 - ignore duplicate histogram: " << name << endl;
    }

    h->SetDirectory(0);
    h->Sumw2();
  }

  return h;
}

//-----------------------------------------------------------------------------
void Msl::IExecAlg::AddTH1(TH1 *h)
{
  if(h) {
    if(!fHists.insert(HistMap::value_type(std::string(h->GetName()), h)).second) {
      log() << "AddTH1 - ignore duplicate histogram: " << h->GetName() << endl;
    }
  }
}

//-----------------------------------------------------------------------------
void Msl::IExecAlg::AddTH2(TH2 *h)
{
  if(h) {
    if(!fHists2D.insert(HistMap2D::value_type(std::string(h->GetName()), h)).second) {
      log() << "AddTH2 - ignore duplicate histogram: " << h->GetName() << endl;
    }
  }
}

//-----------------------------------------------------------------------------
void Msl::IExecAlg::AddTH3(TH3 *h)
{
  if(h) {
    if(!fHists3D.insert(HistMap3D::value_type(std::string(h->GetName()), h)).second) {
      log() << "AddTH3 - ignore duplicate histogram: " << h->GetName() << endl;
    }
  }
}

//-----------------------------------------------------------------------------
void Msl::IExecAlg::SetAlgConf(const Registry &reg)
{
  fReg = reg;
}

//-----------------------------------------------------------------------------
void Msl::IExecAlg::RunAlgConf()
{
  DoConf(fReg);
}

//-----------------------------------------------------------------------------
std::ostream& Msl::IExecAlg::log() const
{
  std::cout << fName << "::"; 
  return std::cout; 
}
