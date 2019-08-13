#ifndef _SLPRIMARYGENERATORACTION_H_
#define _SLPRIMARYGENERATORACTION_H_

#include "G4VUserPrimaryGeneratorAction.hh"

#include "globals.hh"

class G4Event;
class G4ParticleGun;

/// Minimal primary generator action to demonstrate the use of GDML geometries

class SLPrimaryGeneratorAction : public G4VUserPrimaryGeneratorAction
{
  public:

    SLPrimaryGeneratorAction();
   ~SLPrimaryGeneratorAction();

   virtual void GeneratePrimaries(G4Event* anEvent);

  private:

    G4ParticleGun* fParticleGun;
};

#endif
