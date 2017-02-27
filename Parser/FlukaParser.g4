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
    : RegionName Integer (unaryBooleanExpression)+
    ;

lattice
    : Lattice ID+
    ;

unaryBooleanExpression
    : LParen unaryBooleanExpression+ RParen
    | Union unaryBooleanExpression
    | (Subtraction | Intersection) (unaryBooleanExpression | ID)
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
