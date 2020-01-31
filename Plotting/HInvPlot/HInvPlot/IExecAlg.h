#ifndef MSL_IEXECALG_H
#define MSL_IEXECALG_H

/**********************************************************************************
 * @Package: HInvPlot
 * @Class  : IExecAlg
 * @Author : Rustem Ospanov
 *
 * @Brief  :
 * 
 *  Base class for algorithms executed in event loop
 * 
 **********************************************************************************/

// C/C++
#include <map>
#include <iostream>

// ROOT
#include "TH1D.h"

// Local
#include "Event.h"
#include "Registry.h"

class TH1;
class TH2;
class TH3;

namespace Msl
{
  //
  // ABC class for event algorithm
  //
  class IExecAlg
  {
  public:

    IExecAlg();
    virtual ~IExecAlg() {}

    virtual void DoConf(const Registry &reg);

    virtual bool DoExec(Msl::Event &) = 0;

    virtual void DoSave(TDirectory *dir);

    void SetName(const std::string &name) { fName = name; }
    void SetType(const std::string &type) { fType = type; }
    
    const std::string &GetAlgName() const { return fName; }
    const std::string &GetType() const { return fType; }

    void SetAlgConf(const Registry &reg);

    void RunAlgConf();

    void   SetPassStatus(bool   p) { fPassStatus = p; }
    void   SetPassWeight(double w) { fPassWeight = w; }

    bool   GetPassStatus() const { return fPassStatus; }
    double GetPassWeight() const { return fPassWeight; }

  protected:

    typedef std::map<std::string, TH1 *> HistMap;
    typedef std::map<std::string, TH2 *> HistMap2D;
    typedef std::map<std::string, TH3 *> HistMap3D;

  protected:

    std::ostream& log() const;

    TH1* GetTH1(const std::string &name, int nbin,  float arr[]);
    TH1* GetTH1(const std::string &name, int nbin,  double xmin, double xmax);
    TH2* GetTH2(const std::string &name, int xnbin, double xmin, double xmax, 
		int ynbin, double ymin, double ymax);
    TH2 *GetTH2(const std::string &name, int nbinx,  float xarr[], int nbiny,  float yarr[]);
    TH3* GetTH3(const std::string &name,
		int xnbin, double xmin, double xmax, 
		int ynbin, double ymin, double ymax,
		int znbin, double zmin, double zmax);
    
    void AddTH1(TH1 *h);
    void AddTH2(TH2 *h);
    void AddTH3(TH3 *h);

  protected:

    bool          fDebug;
    bool          fPrint;
    bool          fUseName;
    
    std::string   fName;
    std::string   fType;

    bool          fPassStatus;
    double        fPassWeight;

    Registry      fReg;

    HistMap       fHists;
    HistMap2D     fHists2D;
    HistMap3D     fHists3D;
  };
}

#endif
