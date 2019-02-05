int TrigSFUnc(){

  TH1F *h=new TH1F("h","h",500,0.0,2.0);
  TH1F *h16=new TH1F("h16","h16",500,0.0,2.0);
  TH1F *h17=new TH1F("h17","h17",500,0.0,2.0);
  TH1F *h18=new TH1F("h18","h18",500,0.0,2.0);
  TH1F *h20=new TH1F("h20","h20",500,0.0,2.0);        
  double p0D = 99.4255;
  double p1D = 38.6145;
  double p0=0.0;
  double p1=0.0;
  TRandom3 rand;
  rand.SetSeed(10);
  
  for(unsigned i=0; i<10000; ++i){
    p0=p0D+ rand.Gaus(0.0,9.12);
    p1=p1D+ rand.Gaus(0.0,8.23);
    h->Fill(0.5*(1+TMath::Erf((150-p0)/(TMath::Sqrt(2)*p1))));
    h16->Fill(0.5*(1+TMath::Erf((160-p0)/(TMath::Sqrt(2)*p1))));
    h17->Fill(0.5*(1+TMath::Erf((170-p0)/(TMath::Sqrt(2)*p1))));
    h18->Fill(0.5*(1+TMath::Erf((180-p0)/(TMath::Sqrt(2)*p1))));
    h20->Fill(0.5*(1+TMath::Erf((200-p0)/(TMath::Sqrt(2)*p1))));                
  }

  std::cout << "mean: " << h->GetMean() << " RMS: " << h->GetRMS() << std::endl;
  std::cout << "mean: " << h16->GetMean() << " RMS: " << h16->GetRMS() << std::endl;
  std::cout << "mean: " << h17->GetMean() << " RMS: " << h17->GetRMS() << std::endl;
  std::cout << "mean: " << h18->GetMean() << " RMS: " << h18->GetRMS() << std::endl;
  std::cout << "mean: " << h20->GetMean() << " RMS: " << h20->GetRMS() << std::endl;      
  h20->Draw();
  
  return 1;
}
//
