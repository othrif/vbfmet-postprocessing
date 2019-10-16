#ifndef VBFANALYSIS_SIGNALSYSTHELPER_H
#define VBFANALYSIS_SIGNALSYSTHELPER_H 1

#include <iostream>
#include <vector>

using namespace std;

class SignalSystHelper{
 public:
  SignalSystHelper( );
  virtual ~SignalSystHelper();

  void initialize();

  std::string getVarName(int category);
};

#endif //> !VBFANALYSIS_SIGNALSYSTHELPER_H   
