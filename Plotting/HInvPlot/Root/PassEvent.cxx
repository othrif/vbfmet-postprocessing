// C/C++
#include <set>
#include <iostream>
#include <fstream>

// ROOT
#include "TH1.h"
#include "TH2.h"
#include "TSystem.h"

// Local
#include "HInvPlot/PassEvent.h"

using namespace std;

//------------------------------------------------------------------------------------------
// CutFlow manager code
//------------------------------------------------------------------------------------------
Msl::CutFlowMan& Msl::CutFlowMan::Instance()
{
  static Msl::CutFlowMan instance;
  return instance;
}

//------------------------------------------------------------------------------------------
void Msl::CutFlowMan::WriteCutFlows(const std::string &path) const
{
  WriteFlows(path, fCutFlows);
  if(fWriteAll) WriteFlowsIndiv(path, fCutFlows);
}

//------------------------------------------------------------------------------------------
void Msl::CutFlowMan::WriteRawFlows(const std::string &path) const
{
  WriteFlows(path, fRawFlows);
}

//------------------------------------------------------------------------------------------
void Msl::CutFlowMan::WriteFlows(const std::string &path, 
				 const std::map<std::string, std::string> &flows) const
{
  //
  // Write all cut-flows into single text file (to avoid disk IO problems at Penn)
  //
  stringstream str;

  //
  // Write Header of document
  //
  str << "\\documentclass[letterpaper,12pt]{article}\n"
      << "\\usepackage{amsmath}    % need for subequations \n"
      << "\\usepackage{graphicx} \n"
      << "\n"
      << "\\usepackage[hmargin=0.25cm]{geometry}\n"
      << "\n"
      << "\\begin{document}\n";

  for(map<string, string>::const_iterator cit = flows.begin(); cit != flows.end(); ++cit) {
    //
    // Find and replace the underscores
    //
    const string cutflow_name = ReplaceUnderscore(cit->first);

    str << "%------------------------------------------------------------------------------------------\n"
	<< "% Algorithm: " << cit->first << "\n "
	<< cutflow_name
	<< "\n"
	<< "$\\newline$ \n"
	<< cit->second
	<< " $\\newline$"
	<< "\n";
  }

  //
  // End document
  //
  str << "\n" 
      << "\\end{document}";

  std::ofstream fos(path.c_str());

  if(fos.is_open()) {
    fos << str.str();
    fos.close();
  }
}

//------------------------------------------------------------------------------------------
void Msl::CutFlowMan::WriteFlowsIndiv(const std::string &path, 
				      const std::map<std::string, std::string> &flows) const
{

  for(map<string, string>::const_iterator cit = flows.begin(); cit != flows.end(); ++cit) {
    //
    // Find and replace the underscores
    //
    stringstream str;

    const string cutflow_name = ReplaceUnderscore(cit->first);

    str << "%------------------------------------------------------------------------------------------\n"
	<< "% Algorithm: " << cit->first << "\n "
	<< cutflow_name
	<< "\n"
	<< "$\\newline$ \n"
	<< cit->second
	<< "\n";

    std::string oname = path+"_"+cit->first+".table";
    std::ofstream fos(oname.c_str());
    
    if(fos.is_open()) {
      fos << str.str();
      fos.close();
    }
  }
}

//------------------------------------------------------------------------------------------
std::string Msl::CutFlowMan::ReplaceUnderscore(std::string str) const
{
  //
  // Replace "_" with " "
  //
  std::string::iterator sit = str.begin();
  
  while(sit != str.end()) {
    if(*sit == '_') {
      *sit = ' ';
    }
    
    ++sit;
  }

  return str;
}

//-----------------------------------------------------------------------------
// PassEvent code
//-----------------------------------------------------------------------------
Msl::PassEvent::PassEvent()
{
}

//-----------------------------------------------------------------------------
Msl::PassEvent::~PassEvent()
{
}

//-----------------------------------------------------------------------------
void Msl::PassEvent::DoConf(const Registry &reg)
{
  //
  // Read configuration
  //
  IExecAlg::DoConf(reg);

  bool tmp_writeAll=false;
  reg.Get("PassEvent::PassAll",     fPassAll     = false);
  reg.Get("PassEvent::PrintRaw",    fPrintRaw    = false);
  reg.Get("PassEvent::PrintEvents", fPrintEvents = false);
  reg.Get("PassEvent::WriteAll",    tmp_writeAll = false);
  reg.Get("PassEvent::Precision",   fPrecision   = 1);

  //
  // Initialize cuts
  //
  vector<string> cuts;
  reg.Get("PassEvent::Cuts", cuts);

  for(unsigned i = 0; i < cuts.size(); ++i) {
    AddCut(cuts.at(i), reg);
  }
  
  //
  // Read sets of samples
  //
  fSets = Mva::ReadSets(reg, "PassEvent::Sets", GetAlgName());

  if(fPrint) {
    log() << "DoConf - read configuration: " << endl
	  << "   PassAll:     " << fPassAll     << endl
	  << "   PrintRaw:    " << fPrintRaw    << endl
	  << "   PrintEvents: " << fPrintEvents << endl;
    
    cout << "   Number of cuts: " << fCuts.size() << endl;
    for(unsigned i = 0; i < fCuts.size(); ++i) { 
      fCuts.at(i).icut.PrintConfig(std::cout, "   ");
    }

    cout << "   Number of sets: " << fSets.size() << endl;

    if(fDebug) {
      for(unsigned i = 0; i < fSets.size(); ++i) { 
	std::cout << "   " << fSets.at(i).GetName() << ":" << endl;
	fSets.at(i).Print(std::cout, "      ");
      }
    }
  }

  CutFlowMan::Instance().SetWriteAll(tmp_writeAll);
}

//-----------------------------------------------------------------------------
bool Msl::PassEvent::DoExec(Event &event)
{
  //
  // Count input events
  //
  fPollInput.CountEvent(event, event.GetWeight());
  
  //
  // Apply cuts
  //
  const double weight = event.GetWeight();
  bool pass = true;

  for(unsigned i = 0; i < fCuts.size(); ++i) {
    Cut &c = fCuts.at(i);
    
    if(c.icut.PassCut(event) != Select::Pass) {
      pass = false;
      break;
    }

    c.poll.CountEvent(event, event.GetWeight());
  }

  //
  // Set status for in-direct clients
  //
  IExecAlg::SetPassStatus(pass);
  IExecAlg::SetPassWeight(event.GetWeight());

  if(pass && fPrintEvents) {
    fEvents.push_back(event);
  }

  if(fPassAll) {
    //
    // Pass all events - restore event weight
    //
    event.SetWeight(weight);
    return true;
  }

  return pass;
}

//-----------------------------------------------------------------------------
void Msl::PassEvent::DoSave(TDirectory *dir)
{
  if(fDebug) {
    log() << "DoSave - print job summary: "   << endl
	  << "   Cuts:      " << fCuts.size() << endl;

    for(unsigned i = 0; i < fCuts.size(); ++i) {
      const Cut &c = fCuts.at(i);
      
      //
      // Print cut
      //
      c.poll.Print(c.icut.GetName());
      
      if(fDebug) {
	c.icut.PrintCounts();
      }
    }
  }

  //
  // Print cutflow table
  //
  if(!fSets.empty() && !fCuts.empty()) {
    cout << "--------------------------------------------------------------------" << endl;
    log() << "DoSave - print cutflow table: " << endl;
    PrintCounts(std::cout, "", false, fPrintRaw);

    if(fPrintEvents) {
      log() << endl << "DoSave - number of events: " << fEvents.size() << endl;    
      PrintEvents(Mva::kData, std::cout);
      PrintEvents(Mva::kqqww, std::cout);
      //PrintEvents(Mva::kWjdt, std::cout);
    }

    //
    // Add this cutflow to global manager
    //
    stringstream cf, rf;
    PrintCounts(cf, "", true, false);
    PrintCounts(rf, "", true, true);

    CutFlowMan::Instance().AddCutFlow(GetAlgName(), cf.str());
    CutFlowMan::Instance().AddRawFlow(GetAlgName(), rf.str());
  }

  //
  // Fill histograms
  //
  const std::vector<Msl::Mva::Sample> &samples = Mva::GetAllSamples();

  for(unsigned i = 0; i < samples.size(); ++i) {
    FillCounts("sample_", Mva::SampleSet(samples.at(i)));
  }

  for(unsigned i = 0; i < fSets.size(); ++i) {
    FillCounts("", fSets.at(i));
  }

  //
  // Save histograms
  //
  IExecAlg::DoSave(dir);
}

//-----------------------------------------------------------------------------
void Msl::PassEvent::AddCut(const std::string &key, const Registry &reg)
{
  //
  // Add and configure new cut
  //
  Registry creg;  
  if(!reg.Get("PassEvent::"+key, creg)) {
    log() << "AddCut - missing registry for key: " << key << endl;
    return;        
  }
  
  //
  // Add new cut
  //
  fCuts.push_back(Cut());

  //
  // Configure new (last) cut
  //
  fCuts.back().icut.InitCut(creg);
  
  if(fPrintRaw) {
    fCuts.back().poll.UseRaw(true);
  }
}

//-----------------------------------------------------------------------------
TH1* Msl::PassEvent::FillCounts(const std::string &pref, const Mva::SampleSet &sample)
{
  //
  // Create histogram
  //
  TH1 *h = GetTH1((pref+sample.GetName()), fCuts.size(), 0.0, fCuts.size());

  h->GetXaxis()->CenterTitle();
  h->GetXaxis()->SetTitle(sample.GetName().c_str());

  for(unsigned i = 0; i < fCuts.size(); ++i) {
    const CutItem &ci = fCuts.at(i).icut;
    const CutPoll &cp = fCuts.at(i).poll;

    h->GetXaxis()->SetBinLabel(i+1, ci.GetName().c_str());

    //
    // Collect indi
    //
    double val = 0.0, err = 0.0;
    
    if(cp.GetCountError(sample, val, err)) {
      //
      // Set passed number of events and error
      //
      h->SetBinContent(i+1, val);
      h->SetBinError  (i+1, err);
    }
  }

  return h;
}

//-----------------------------------------------------------------------------
void Msl::PassEvent::PrintCounts(std::ostream &os, 
				 const std::string &pad, 
				 const bool writeTex,
				 const bool writeRaw)
{
  //
  // Print cutflow table for sets of samples
  //
  if(fSets.empty()) {
    return;
  }

  if(writeRaw) {
    fPollInput.UseRaw(true);

    for(unsigned i = 0; i < fCuts.size(); ++i) {
      fCuts.at(i).poll.UseRaw(true);
    }
  }

  std::string pm       = " +/- ";
  std::string amb      = "  ";
  std::string end_line = "\n";
  std::string sep_line = "";
  //float bkg_val = 0.0;
  //float data_val = 0.0;

  if(writeTex) {
    pm       = " $\\pm$ ";
    amb      = "&  ";
    end_line = " \\\\ \n";
    sep_line = "\\hline\\hline\n";

    os << "\\resizebox{\\textwidth}{!} { \n";
	     
    os << "\\begin{tabular}{";
    bool first=true;
    for(unsigned s = 0; s < fSets.size()+1; ++s) {
      if(first){  os << "l||"; first=false; }
      else if(s!=fSets.size()) os << "l"; 
      else os << "|l"; 
    }
    os << "}\n";
  }

  //
  // Compute margins
  //
  ComputePads(writeTex);

  //
  // Compute cell width for all rows and columns
  //
  unsigned namew = string("Input").size();

  for(unsigned i = 0; i < fCuts.size(); ++i) {
    const Cut &c = fCuts.at(i);

    //
    // Find maximum width for cut name
    //
    namew = std::max<unsigned>(namew, c.icut.GetName().size());
  }

  //
  // Write column headers
  //
  os << sep_line << pad << setw(namew) << " " << amb;

  for(unsigned s = 0; s < fSets.size(); ++s) {
    std::string sample_name = fSets.at(s).GetName();
    
    if(writeTex) { 
      sample_name = Mva::Convert2Tex(fSets.at(s));
    }

    const Pad pd = FillPad(fSets.at(s));
    
    os << left << setw(pd.GetCellWidth(pm)) << sample_name;

    if(s+1 < fSets.size()){
      os << amb;
    }
    else{
      os << end_line;
    }
    
  } 

  //
  // Print input events
  //
  os << sep_line << pad << setw(namew) << left << "Input" << amb;

  for(unsigned s = 0; s < fSets.size(); ++s) {
    const pair<string, string> ires = fPollInput.GetCountErrorAsPair(fSets.at(s), fPrecision);
    
    const Pad pd = FillPad(fSets.at(s));    

    //
    // Write one cell
    //
    stringstream cell;

    cell << "" 
	 << setw(pd.valw) << left << ires.first  << pm
	 << setw(pd.errw) << left << ires.second;   

    for(unsigned p = cell.str().size(); p < pd.GetCellWidth(pm); ++p) {
      cell << " ";
    }

    if(s+1<fSets.size()){
      cell << amb;
    }
    else{
      cell << end_line;
    }
    
    os << cell.str();
  }

  //
  // Print table
  //
  for(unsigned i = 0; i < fCuts.size(); ++i) {
    const Cut &c = fCuts.at(i);

    os << pad << setw(namew) << c.icut.GetName() << amb;

    for(unsigned s = 0; s < fSets.size(); ++s) {
      const pair<string, string> res = c.poll.GetCountErrorAsPair(fSets.at(s), fPrecision);

      const Pad pd = FillPad(fSets.at(s));
      
      //
      // Write one cell
      //
      stringstream cell;
      
      cell << "" 
	   << setw(pd.valw) << left << res.first  << pm
	   << setw(pd.errw) << left << res.second;   
      
      for(unsigned p = cell.str().size(); p < pd.GetCellWidth(pm); ++p) {
	cell << " ";
      }
      
      if(s+1<fSets.size()){
	cell << amb;
      }
      else{
	cell << end_line;
      }
    
      os << cell.str();
    }
  }

  if(fDebug) {
    //
    // Print scale factor names
    //
    for(unsigned i = 0; i < fCuts.size(); ++i) {
      const Cut &c = fCuts.at(i);
      const std::vector<Msl::Mva::Var> &vars = c.icut.GetWeightVars();
      
      if(vars.empty()) {
	continue;
      }
      
      os << pad << setw(namew) << c.icut.GetName() << ":";
      
      for(unsigned j = 0; j < vars.size(); ++j) {
	os << " " << Mva::AsStr(vars.at(j));
      }

      os << endl;
    }
  }

  os << sep_line;

  if(writeTex) {
    os << "\\end{tabular}\n"
       << "}\n";
  }
}

//-----------------------------------------------------------------------------
void Msl::PassEvent::ComputePads(const bool writeTex)
{
  //
  // Compute cell width for all rows and columns
  //
  for(unsigned i = 0; i < fCuts.size(); ++i) {
    const Cut &c = fCuts.at(i);

    for(unsigned s = 0; s < fSets.size(); ++s) {
      const pair<string, string> res = c.poll.GetCountErrorAsPair(fSets.at(s), fPrecision);     
      
      //
      // Find maximum field width for count and error 
      //
      PadMap::iterator pit = fPads.insert(PadMap::value_type(fSets.at(s).GetName(), Pad())).first;

      pit->second.valw = std::max<unsigned>(pit->second.valw, res.first .size());
      pit->second.errw = std::max<unsigned>(pit->second.errw, res.second.size());

      //
      // Find maximum field width for count and error for input events
      //
      const pair<string, string> ires = fPollInput.GetCountErrorAsPair(fSets.at(s), fPrecision);
      
      pit->second.valw = std::max<unsigned>(pit->second.valw, ires.first .size());
      pit->second.errw = std::max<unsigned>(pit->second.errw, ires.second.size());

      //
      // Compute width of cell header
      //
      std::string sample_name = fSets.at(s).GetName();
      
      if(writeTex) { 
	sample_name = Mva::Convert2Tex(fSets.at(s));
      }

      pit->second.hdrw = std::max<unsigned>(pit->second.hdrw, sample_name.size());
    }    
  }
}

//-----------------------------------------------------------------------------
Msl::PassEvent::Pad Msl::PassEvent::FillPad(const Mva::SampleSet &s) const
{
  //
  // Fill padding values for one column
  //
  const PadMap::const_iterator pit = fPads.find(s.GetName());
  
  if(pit != fPads.end()) {
    return pit->second;
  }
  
  return Pad();
}

//-----------------------------------------------------------------------------
void Msl::PassEvent::PrintEvents(const Mva::Sample &sample, std::ostream &os) const
{
  //
  // Print saved event list
  //
  unsigned icount = 0;

  for(unsigned i = 0; i < fEvents.size(); ++i) {
    //
    // Print events
    //
    const Event &event = fEvents.at(i);
    
    if(sample == event.sample) {
      icount++;
      os << std::setw( 6)   << event.RunNumber   << ", "
    	 << std::setw(10)   << event.EventNumber << ", "
    	 << endl;
    }
  }
  
  os << "PrintEvents - printed " << icount << " event(s)" << endl;
}
