#include <G4Electron.hh>
#include "globals.hh" // geant4 types / globals
#include "G4AutoDelete.hh"
#include "G4Electron.hh"
#include "G4PhysicsListHelper.hh"
#include "SLPhysicsList.hh"

SLPhysicsList::SLPhysicsList():
        G4VUserPhysicsList()
{;}

SLPhysicsList::~SLPhysicsList(){;}

void SLPhysicsList::ConstructParticle()
{
    G4Electron::ElectronDefinition();
}

void SLPhysicsList::ConstructProcess(){
     AddTransportation();
    }
void SLPhysicsList::SetCuts() {;}