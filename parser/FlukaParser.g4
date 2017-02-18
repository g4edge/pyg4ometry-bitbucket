parser grammar FlukaParser ;

options {
    tokenVocab=FlukaLexer;
//    language=Python2 ;
}


model
    : command+ ;

command
    // : geoCommand
    : GeoBegin geo GeoEnd
    ;

// /* Geometry rules: */
// geoCommand
//     : geoCard
//     | geoDirective
//     ;

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
    | BodyCode GeoID Float+
    | BodyCode (Delim (GeoID|Float)?)*
    ;

region
    : RegionName Integer (booleanExpression)+
    ;

lattice
    : Lattice GeoID+
    ;

// booleanExpression
//     : LParen booleanExpression RParen
//     | Complement booleanExpression (Complement booleanExpression)*
//     | ((Intersection|Subtraction) GeoID)+
//     ;

booleanExpression
    : LParen booleanExpression+ RParen
    | Complement booleanExpression
    | (Subtraction | Intersection) (booleanExpression | GeoID)
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
    : StartTranslat Float Float Float body+ EndTranslat
    ;

transform
    : StartTransform (GeoID | Integer) body+ EndTransform
    ;


// pre_directive
//     : if (command | pre_directive)+ endif
//     | elif (command | predirective)+
//     | define
//     ;

// if


/* End Geometry rules */
