parser grammar FlukaParser ;

options {
tokenVocab=FlukaLexer;
language=Python2 ;
}


model
    : command+
    ;

command
    : geoBegin geocards GeoEnd
    ;

geoBegin
    : GeoBegin (Float | Integer | ID)*
    ;

geocards
    : (body | region | lattice)+
    ;

body
    : geoDirective                     # GeometryDirective
    | BodyCode (ID | Integer) Float+   # BodyDefSpaceDelim
    | BodyCode (Delim (ID|Float)?)*    # BodyDefPunctDelim
    ;

region
    : RegionName Integer zone
    | RegionName Integer zoneUnion
    ;

zone
    : booleanExpression
    | subZone
    ;

subZone
    : (Minus | Plus)? LParen booleanExpression RParen
    ;

zoneUnion
    : Bar zone (Bar zone)+
    ;

booleanExpression
    : unaryExpression
    | unaryExpression booleanExpression
    | unaryExpression subZone
    | booleanExpression Bar booleanExpression
    ;

unaryExpression
    : (Minus | Plus) ID
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
    : StartTransform (ID | Integer) body+ EndTransform
    ;

lattice
    : Lattice ID+
    ;
