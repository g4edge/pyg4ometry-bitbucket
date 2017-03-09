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

zoneUnion
    : Bar zone (Bar zone)+
    ;

zone
    : expr
    | subZone
    ;

subZone
    : (Minus | Plus) LParen expr RParen
    ;

expr
    : unaryExpression         # singleUnary
    | unaryExpression expr    # unaryAndBoolean
    | unaryExpression subZone # unaryAndSubZone
    | expr Bar expr           # booleanBarBoolean
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
