void getN(TString file){
  TFile *f = new TFile(file,"READ"); 

  cout << elem->GetTitle() << endl;
  TString fname = elem->GetTitle();
  
  TObjArray *dsid_obj = (TObjArray*)fname.Tokenize(".");
  
  TObjString *tmp = (TObjString*)dsid_obj->At(3);
  TString dsid_string = tmp->GetString();
  //cout << dsid_string << endl;                                                                                                                                
  
  TH1F *h = (TH1F*)f->Get("NumberEvents");
  h_total->Fill(dsid_string,h->GetBinContent(2));
  //cout << "N " << h->GetBinContent(2) << endl;                                                                                                                
  delete f;
}
