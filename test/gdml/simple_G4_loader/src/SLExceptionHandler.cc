#include "SLExceptionHandler.hh"
#include "G4ExceptionHandler.hh"

SLExceptionHandler::SLExceptionHandler():
        G4VExceptionHandler()
{;}

SLExceptionHandler::~SLExceptionHandler(){;}

G4bool SLExceptionHandler::Notify(const char *originOfException, const char *exceptionCode, G4ExceptionSeverity severity,
                                const char *description) {
    (void)originOfException;
    (void)severity;

    G4cerr << "ERROR! " << description << G4endl;

    if (std::strcmp(exceptionCode, "GeomVol1002") == 0){
        G4cout << description << G4endl;
        G4cout << "Error! Overlaps detected in geometry" << G4endl;
        throw std::exception();
    }

    return true;

}