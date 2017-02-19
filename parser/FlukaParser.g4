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
    : geoCard+
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
