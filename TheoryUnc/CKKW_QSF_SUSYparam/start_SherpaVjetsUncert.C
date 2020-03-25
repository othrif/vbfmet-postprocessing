void start_SherpaVjetsUncert( TString suffix = "all", int nentries = -1, TString directory = "./merged") {
 TChain * chain = new TChain("", "");

 std::cout << "Start" << std::endl;
 chain->Add(directory + "_mc16a/Z_strong.root/Z_strongNominal");
 chain->Add(directory + "_mc16d/Z_strong.root/Z_strongNominal");
 chain->Add(directory + "_mc16e/Z_strong.root/Z_strongNominal");
 chain->Add(directory + "_mc16a/W_strong.root/W_strongNominal");
 chain->Add(directory + "_mc16d/W_strong.root/W_strongNominal");
 chain->Add(directory + "_mc16e/W_strong.root/W_strongNominal");
 if(nentries == -1)
    nentries = chain->GetEntries();
 chain->Process("MySelector.C",suffix,nentries);
 std::cout << "End" << std::endl;
}
