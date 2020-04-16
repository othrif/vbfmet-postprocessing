
#include <TSystem.h>
#include <TProof.h>
#include <TProofLog.h>
#include <THashList.h>
#include "TStopwatch.h"

void runSkim(TString inputDir="/nfs/dust/atlas/user/othrif/samples/MicroNtuples/v35Truth/", TString outputDir="/nfs/dust/atlas/user/othrif/scratch/myPP/latest/processed", TString process="W_EWK", long long num = -1, TString debug = "false") {

  TStopwatch p;
  p.Start();

  TChain * chain;
  TString options;

  std::cout << "\nProcessing " << process << "..." << std::endl;
  chain = new TChain("", "");
  chain->Add(inputDir+"/"+process+".root/"+process+"Nominal");
   if(num == -1)
    num = chain->GetEntries();
  options =  TString::Format("%lld", chain->GetEntries())+","+outputDir+","+process+","+debug;
  chain->Process("slimSkim.C+",options);
  delete chain;
  std::cout << "Output file: " << outputDir << "/" << process << ".root" << std::endl;
  std::cout << "Done processing " << process << ".\n" << std::endl;

  p.Stop();
  p.Print();

}
