// Local
#include "HInvPlot/VarEntry.h"

using namespace std;

//--------------------------------------------------------------------------------------      
Msl::VarEntry::VarEntry() :
  fKey (0),
  fData(0.0)
{
}

//--------------------------------------------------------------------------------------      
Msl::VarEntry::VarEntry(const unsigned int key, const double data) :
  fKey (key),
  fData(data)
{
}

//--------------------------------------------------------------------------------------      
void Msl::VarEntry::Print(std::ostream &os) const
{
  os << "VarEntry::Print" << std::endl;
}
