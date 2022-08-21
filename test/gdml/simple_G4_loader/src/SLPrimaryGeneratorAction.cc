#include "SLPrimaryGeneratorAction.hh"
#include "G4Event.hh"
#include "G4ParticleGun.hh"
#include "G4ParticleTable.hh"
#include "G4ParticleDefinition.hh"
#include "G4SystemOfUnits.hh"

#include "Randomize.hh"

SLPrimaryGeneratorAction::SLPrimaryGeneratorAction()
 : G4VUserPrimaryGeneratorAction(),
   fParticleGun(0)
{
  G4int n_particle = 1;
  fParticleGun = new G4ParticleGun(n_particle);

  G4ParticleTable* particleTable = G4ParticleTable::GetParticleTable();
  G4String particleName;
  fParticleGun->SetParticleDefinition(
               particleTable->FindParticle(particleName="e-"));

  fParticleGun->SetParticleEnergy(1*GeV);
  fParticleGun->SetParticlePosition(G4ThreeVector(0, 0, 0));
}

SLPrimaryGeneratorAction::~SLPrimaryGeneratorAction()
{
  delete fParticleGun;
}


void SLPrimaryGeneratorAction::GeneratePrimaries(G4Event* anEvent)
{
    G4double u1 = 1;
    G4double u2 = 1;
    while(std::pow(u1,2) + std::pow(u2,2) >= 1){ // Isotropic distribution - Marsaglia method
        u1 = G4RandFlat::shoot(-1, 1);
        u2 = G4RandFlat::shoot(-1, 1);
    }

    G4double x = 2*u1*std::sqrt(1 - std::pow(u1, 2) - std::pow(u2, 2));
    G4double y = 2*u2*std::sqrt(1 - std::pow(u1, 2) - std::pow(u2, 2));
    G4double z = 1 - 2*(std::pow(u1, 2) + std::pow(u2, 2));
    G4ThreeVector v(x,y,z);

  fParticleGun->SetParticleMomentumDirection(v);
  fParticleGun->GeneratePrimaryVertex(anEvent);
}
