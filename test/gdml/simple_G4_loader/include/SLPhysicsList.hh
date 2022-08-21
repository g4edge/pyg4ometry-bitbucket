#ifndef SLPHYSICSLIST_H
#define SLPHYSICSLIST_H

#include "globals.hh" // geant4 types / globals
#include "G4VUserPhysicsList.hh"

class SLPhysicsList: public G4VUserPhysicsList
{
public:
    SLPhysicsList();
    virtual ~SLPhysicsList();
    virtual void ConstructParticle();
    virtual void ConstructProcess();
    virtual void SetCuts();
};

#endif