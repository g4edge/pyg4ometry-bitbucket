lexer grammar FlukaLexer;

tokens{Integer,
    Float,
    ID,
    Delim
}

// This is the default mode.

InLineComment
    : '!' ~[\r\n]*
	-> skip
    ;

Whitespace
    : [ \t]
	->skip
    ;

// Currently skipping preprocessor directives.
LineComment
    : ('*'|'#') {self.column == 1}? ~[\r\n]*
	-> skip
    ;

GeoBegin
    : 'G' {self.column == 1}? 'EOBEGIN' ~[\r\n]*
	-> pushMode(geometry)
    ;

Keyword
    : [A-Za-z] {self.column == 1}? [A-Za-z0-9_-]+
	-> skip
    ;

ID
    : [A-Za-z@] {self.column != 1}? [A-Za-z0-9_-]*
	-> skip
    ;

Newline
    : '\r'? '\n'
	-> skip
    ;

Integer
    : '-'? Digit+ -> skip
    ;

Float
    : ('+' | '-'?)
	( // (1.3 | 1. | 1E5 | 1.E5 | 0041E5 | 1.14E+04
	    Digit+ '.'? Digit* 'E'? ('+'|'-')? Digit*
	|
	    '.' Digit+  // .123
	)
	-> skip
    ;

fragment
Digit
    : [0-9]
    ;

Delim : [,:;/]
	-> skip
    ;

mode geometry;

GeoEnd
    : 'G' {self.column == 1}? 'EOEND'
	-> popMode
    ;

End
    : 'E' {self.column == 1}? 'ND'
    -> skip
    ;

BodyCode
    : [A-Z] {self.column == 1}? [A-Z] [A-Z]
    ;

Lattice
    : 'L' {self.column == 1}? 'ATTICE'
    ;

RegionName
    : [A-Za-z] {self.column == 1}? [A-Za-z0-9_]+
    ;
// $Start_expansion takes precedence over $Start_translat, which in turn takes
// precedence over $Start_transform.  Leave this until the visitor to resolve (?)

// Geometry directives:
StartExpansion
    : '$' {self.column == 1}? 'start_expansion'
    ;

StartTranslat
    :  '$' {self.column == 1}? 'start_translat'
    ;

StartTransform
    : '$' {self.column == 1}? 'start_transform'
    ;

EndExpansion
    : '$' {self.column == 1}? 'end_expansion'
    ;

EndTranslat
    : '$' {self.column == 1}? 'end_translat'
    ;

EndTransform
    :'$' {self.column == 1}? 'end_transform'
    ;

GeoInteger
    : '-'? GeoDigit+ ->type(Integer)
    ;

GeoFloat
    : ('+' | '-'?)
	( // (1.3 | 1. | 1E5 | 1.E5 | 0041E5 | 1.14E+04
	    GeoDigit+ '.'? GeoDigit* 'E'? ('+'|'-')? GeoDigit*
	|
	    '.' GeoDigit+  // .123
	)
	-> type(Float)
    ;

fragment
GeoDigit
    : [0-9]
    ;


GeoNewline
    : '\r'? '\n'
	-> channel(HIDDEN)
    ;

GeoWhitespace
    : [ \t]
	->skip
// 	->channel(HIDDEN)
    ;

// A GeoID does not start at the beginning of the line.
GeoID
    : [A-Za-z] {self.column != 1}? [A-Za-z0-9_-]*
	-> type(ID)
    ;

GeoInLineComment
    : '!' ~[\r\n]*
	-> skip
    ;

// Currently skip preprocessor directives.
GeoLineComment
    : ('*'|'#') {self.column == 1}? ~[\r\n]*
	-> skip
    ;

GeoDelim
    : [,:;/]
	-> type(Delim)
    ;
Intersection : '+' ;
Subtraction  : '-' ;
Complement   : '|' ;
LParen       : '(' ;
RParen       : ')' ;
