// Othmane Rifki
// usage: root interploate.cxx
// simple macro to do an interpolation, calculate the transfer factor uncertainty between SR and CR, and plot the results


void interpolate(){

const int n = 5;
Double_t x[n] = {0.9, 1.25, 1.75, 2.75, 4.25};

const int n1 = 5;
Double_t x1[n1] = {0.9, 1.25, 1.75, 2.75, 4.25};
Double_t y1[n1] = {1.0157,1.0152,1.0248,1.0344,1.05096};
const int n2 = 5;
Double_t x2[n2] = {0.9, 1.25, 1.75, 2.75, 4.25};
Double_t y2[n2] = {1.0152,1.0151,1.0176,1.0235,1.03021};


Double_t yy[n];
for(int i=0; i<n1; i++){
yy[i] = fabs((y1[i])/(y2[i])-1)*100.0;
std::cout << "Bin " << i << " " << y1[i] << "/" << y2[i] << " > " << yy[i] << std::endl;
}

TGraph *plot1 = new TGraph(n1,x1,y1);
plot1->SetLineColor(kRed);
plot1->GetYaxis()->SetRangeUser(1.0,1.3);
plot1->Draw("AL*");
plot1->Fit("pol1");
TF1 *f1 = plot1->GetFunction("pol1");
f1->SetLineColor(kRed);
f1->SetLineWidth(1);

TGraph *plot2 = new TGraph(n2,x2,y2);
plot2->SetLineColor(kBlue);
plot2->Draw("same L*");
plot2->Fit("pol1");
TF1 *f2 = plot2->GetFunction("pol1");
f2->SetLineColor(kBlue);
f2->SetLineWidth(1);

for(int i=0; i<n; i++){
yy[i] = fabs((y1[i])/(y2[i])-1)*100.0;
std::cout << "Bin " << i << " " << y1[i] << "/" << y2[i] << " > " << yy[i] << std::endl;
}

std::cout << "===========" << std::endl;
std::cout << "SR" << std::endl;
for(int i=0; i<n; i++) std::cout << y1[i]<< ",";
std::cout << std::endl;
for(int i=0; i<n; i++) std::cout << 2-y1[i]<< ",";
std::cout << std::endl;
std::cout << "===========" << std::endl;
std::cout << "CR" << std::endl;
for(int i=0; i<n; i++) std::cout << y2[i]<< ",";
std::cout << std::endl;
for(int i=0; i<n; i++) std::cout << 2-y2[i]<< ",";
std::cout << std::endl;

TLegend *leg = new TLegend(0.3, 0.7, 0.65, 0.9);
leg->AddEntry(plot1, "SR", "l");
leg->AddEntry(plot2, "CR", "l");
leg->Draw();

}