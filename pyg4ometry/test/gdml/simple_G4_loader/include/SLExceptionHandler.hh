#ifndef SLEXCEPTIONHANDLER_H
#define SLEXCEPTIONHANDLER_H

#include "G4ExceptionHandler.hh"

class SLExceptionHandler: public G4VExceptionHandler {
public:
    SLExceptionHandler();
    virtual ~SLExceptionHandler();
    G4bool Notify(const char *originOfException, const char *exceptionCode, G4ExceptionSeverity severity,
                                    const char *description);
};

#endif