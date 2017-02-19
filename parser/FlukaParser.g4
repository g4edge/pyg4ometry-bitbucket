parser grammar FlukaParser ;

options {
    tokenVocab=FlukaLexer;
//    language=Python2 ;
}


model
    : command+ ;

command
    : geoBegin geo GeoEnd
    ;

geoBegin
    : GeoBegin (Float | Integer | ID)*
    ;

geo
    : /*GeoBegin*/ geoCard+ // GeoEnd
    ;

geoCard
    : body
    | region
    | lattice
    ;

body
    : geoDirective
    | BodyCode (ID | Integer) Float+
    | BodyCode (Delim (ID|Float)?)*
    ;

region
    : RegionName Integer (booleanExpression)+
    ;

lattice
    : Lattice ID+
    ;

// booleanExpression
//     : LParen booleanExpression RParen
//     | Complement booleanExpression (Complement booleanExpression)*
//     | ((Intersection|Subtraction) ID)+
//     ;

booleanExpression
    : LParen booleanExpression+ RParen
    | Complement booleanExpression
    | (Subtraction | Intersection) (booleanExpression | ID)
    ;

geoDirective
    : expansion
    | translat
    | transform
    ;

expansion
    : StartExpansion Float body+ EndExpansion
    ;

translat
    : StartTranslat (Float Float Float | Integer) body+ EndTranslat
    ;

transform
    : StartTransform (ID | Integer) body+ EndTransform
    ;


// pre_directive
//     : if (command | pre_directive)+ endif
//     | elif (command | predirective)+
//     | define
//     ;

// if


/* End Geometry rules */
