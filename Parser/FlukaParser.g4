parser grammar FlukaParser ;

options {
tokenVocab=FlukaLexer;
language=Python2 ;
}

// Fluka cards either have a "special" (typically multi-line) form, or
// consist of just a single card.  All commands will be initially be
// assumed to consist of a single card and so will be matched by the
// rule otherKeywords.

// Code for specific single-card commands can then be added to the
// otherKeywords parser rule.  This is preferable to creating a new
// rule for every single command.

// For commands which span multiple cards, such as MATERIAL (which may
// or may not be followed by 1 or more COMPOUND cards), specific rules
// need to be defined in the following manner:

// 1.  Add the lexer rule for the keyword in FlukaLexer.g4, following
// the pattern used by, for example, MATERIAL recalling that for two
// equally matching rules, the one that comes first in the file will
// be matched.  This means, write it above the Keyword lexer rule!

// 2.  Add a corresponding parser rule to "command" in
// FlukaParser.g4.

// 3.  Regenerate the lexer, parser, listener, and visitor, and then
// add the relevant code to the rules.

model
    : command+
    ;

command
    : material_declr
    | geoBegin geocards GeoEnd
    | otherKeywords // Single-card commands.
    ;

// Commands
material_declr
    : material              # SimpleMaterial
    | material compound+    # CompoundMaterial
    ;

material
    : Material (Float | Integer | ID)+
    ;

compound
    : Compound (Float | Integer | ID)+
    ;

geoBegin
    : GeoBegin (Float | Integer | ID)*
    ;

otherKeywords
    : Keyword (Float | Integer | ID)*
    ;

// Geometry:
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
    : Bar zone (Bar zone)+ # multipleUnion
    | Bar zone             # singleUnion
    ;

zone
    : expr
    | subZone
    ;

subZone
    : (Minus | Plus) LParen (expr | binaryUnion) RParen
    ;

expr
    : unaryExpression         # singleUnary
    | unaryExpression expr    # unaryAndBoolean
    | unaryExpression subZone # unaryAndSubZone
    | subZone+                # multipleSubZones
    ;

binaryUnion
    : expr Bar expr
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
