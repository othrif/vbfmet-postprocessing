
// Local
#include "HInvPlot/RecParticle.h"

using namespace std;

//-----------------------------------------------------------------------------
Msl::RecParticle::RecParticle():
  eta           (0.0),
  phi           (0.0),
  pt            (0.0),
  m             (0.0),
  bits          (0)
{
}

//-----------------------------------------------------------------------------
void Msl::RecParticle::Clear()
{
  //
  // Clear vector of variables
  //
  VarHolder::ClearVars();
  eta           = 0.0;
  phi           = 0.0;
  pt            = 0.0;
  m             = 0.0;
  bits          = 0;

}

//-----------------------------------------------------------------------------
void Msl::RecParticle::Print() const
{
  cout << "RecParticle::Print"   << endl
       << "   Eta:            " << eta           << endl
       << "   Phi:            " << phi           << endl
       << "   Pt:             " << pt            << endl
       << "   M:              " << m             << endl;
}
