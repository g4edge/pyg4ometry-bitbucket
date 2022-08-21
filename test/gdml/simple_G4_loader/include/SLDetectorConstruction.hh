#ifndef _SLDETECTORCONSTRUCTION_H_
#define _SLDETECTORCONSTRUCTION_H_

#include "G4VUserDetectorConstruction.hh"

/// Detector construction allowing to use the geometry read from the GDML file

class SLDetectorConstruction : public G4VUserDetectorConstruction
{
  public:
 
    SLDetectorConstruction(G4VPhysicalVolume *setWorld = 0)
    {   
      fWorld = setWorld;
    }

    virtual G4VPhysicalVolume *Construct()
    {
      return fWorld;
    }

  private:

    G4VPhysicalVolume *fWorld;
};

#endif
