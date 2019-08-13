#include <vector>

#include "G4RunManager.hh"
#include "G4UImanager.hh"

#include "G4TransportationManager.hh"

#include "SLPrimaryGeneratorAction.hh"
#include "SLDetectorConstruction.hh"
#include "SLPhysicsList.hh"
#include "SLExceptionHandler.hh"
#include "FTFP_BERT.hh"

#include "G4GDMLParser.hh"

#ifdef G4VIS_USE
#include "G4VisExecutive.hh"
#endif

#ifdef G4UI_USE
#include "G4UIExecutive.hh"
#endif

int main(int argc,char **argv)
{
   G4cout << G4endl;
   G4cout << "Usage: load_gdml <input_gdml_file:mandatory> <visualise_flag:optional>" << G4endl;
   G4cout << G4endl;

   if (argc<2)
   {
      G4cout << "Input file is not specified." << G4endl;
      G4cout << G4endl;
      return -1;
   }

   G4GDMLParser parser;
    parser.SetOverlapCheck(true);

// Uncomment the following if wish to avoid names stripping
// parser.SetStripFlag(false);
    new SLExceptionHandler(); // Throws an exception if there are overlaps

    try {
        parser.Read(argv[1]);
    }
    catch(const std::exception&){ // Overlaps detected
        return 7;                 // Note that other failures do not throw c++
                                  // exceptions, but rather Geant4 errors
    }
   
   if (argc > 4)
   {
      G4cout << "Too many argument." << G4endl;
      G4cout << G4endl;
      return -1;
   }

   G4RunManager* runManager = new G4RunManager;

   runManager->SetUserInitialization(new SLDetectorConstruction(
                                     parser.GetWorldVolume()));

    if(argc == 4 && atof(argv[3])){
        runManager->SetUserInitialization(new FTFP_BERT);
    }
    else {
        runManager->SetUserInitialization(new SLPhysicsList);
    }

   runManager->SetUserAction(new SLPrimaryGeneratorAction);

   runManager->Initialize();

    //Visualisation
    if (argc >= 3 && atof(argv[2])) {
        G4UImanager *UImanager = G4UImanager::GetUIpointer();
#ifdef G4UI_USE
        G4UIExecutive *ui = new G4UIExecutive(argc, argv);
#ifdef G4VIS_USE
        G4VisManager *visManager = new G4VisExecutive;
        visManager->Initialize();
        UImanager->ApplyCommand("/control/execute vis.mac");
#endif
        ui->SessionStart();
#ifdef G4VIS_USE
        delete visManager;
#endif
        delete ui;
#endif
    }
    else {
        runManager->BeamOn(1000);
    }

   delete runManager;

   return 0;
}

   
