lexer grammar FlukaLexer;

// @lexer::members {
//     int lastTokenType = 0;
//     public void emit(Token token) {
// 	super.emit(token);
// 	lastTokenType = token.getType();
//     }
// }



// Atoms.
// InLineCommentNorm
//     : '!' ~[\r\n]*
// 	-> skip
//     ;

// // Currently skip preprocessor directives.
// LineCommentNorm
//     : '*' {getCharPositionInLine() != 1}? ~[\r\n]*
// 	-> skip
//     ;


GeoBegin
    : .*? 'GEOBEGIN' ~[\r\n]*
	-> pushMode(geometry) // , skip
    ;

// GeoBegin
//     : GeoStart GeoTitle
// 	-> mode(geometry)
//     ;

// fragment
// GeoStart
//     :  .*? ('GEOBEGIN'|EOF) ~[\r\n]*
//     ;
// GeoTitle
//     : ~[\r\n

// AfterGeo
//     :

mode ignoreRest;

Stuff : .*? EOF -> skip ;

mode geometry;

GeoEnd
    : 'G' {getCharPositionInLine() == 1}? 'EOEND'
	-> mode(ignoreRest) // , skip
    ;

// GeoTitle
//      : .*? '\n' // {lastTokenType == GeoBegin}? ~[\r\n]*
//      ;

End
    : 'E' {getCharPositionInLine() == 1}? 'ND'
    -> skip
    ;

BodyCode
    : [A-Z] {getCharPositionInLine() == 1}? [A-Z] [A-Z]
    ;

Lattice
    : 'L' {getCharPositionInLine() == 1}? 'ATTICE'
    ;

RegionName
    : [A-Za-z] {getCharPositionInLine() == 1}? [A-Za-z0-9_]+
    ;
// $Start_expansion takes precedence over $Start_translat, which in turn takes
// precedence over $Start_transform.  Leave this until the visitor to resolve (?)

// Geometry directives:
StartExpansion
    : '$' {getCharPositionInLine() == 1}? 'start_expansion'
    ;

StartTranslat
    : /* '$' {getCharPositionInLine() == 1}? */ '$start_translat'
    ;

StartTransform
    : '$' {getCharPositionInLine() == 1}? 'start_transform'
    ;
//  How about sending them to another channel?

EndExpansion
    : '$' {getCharPositionInLine() == 1}? 'end_expansion'
    ;

EndTranslat
    : '$' {getCharPositionInLine() == 1}? 'end_translat'
    ;

EndTransform
    :'$' {getCharPositionInLine() == 1}? 'end_transform'
    ;

Integer
    : '-'? Digit+
    ;

Float
    : '-'?
	( // (1.3 | 1. | 1E5 | 1.E5 | 0041E5 | 1.14E+04
	    Digit+ '.'? Digit* 'E'? ('+'|'-')? Digit*
	|
	    '.' Digit+  // .123
	)
    ;

fragment
Digit
    : [0-9]
    ;


Newline
    : '\r'? '\n'
	-> channel(HIDDEN)
    ;

Whitespace
    : [ \t]
	->channel(HIDDEN)
    ;

// An ID does not start at the beginning of the line.
ID
    : [A-Za-z] {getCharPositionInLine() != 1}? [A-Za-z0-9_]*
    ;

// Atoms.
InLineComment
    : '!' ~[\r\n]*
	-> skip
    ;

// Currently skip preprocessor directives.
LineComment
    : ('*'|'#') {getCharPositionInLine() == 1}? ~[\r\n]*
	-> skip
    ;

Delim
    : [,:;/]
    ;

Intersection: '+' ;
Subtraction : '-' ;
Complement : '|' ;
LParen : '(' ;
RParen : ')' ;

/* case insensitive lexer matching */
// fragment A:('a'|'A');
// fragment B:('b'|'B');
// fragment C:('c'|'C');
// fragment D:('d'|'D');
// fragment E:('e'|'E');
// fragment F:('f'|'F');
// fragment G:('g'|'G');
// fragment H:('h'|'H');
// fragment I:('i'|'I');
// fragment J:('j'|'J');
// fragment K:('k'|'K');
// fragment L:('l'|'L');
// fragment M:('m'|'M');
// fragment N:('n'|'N');
// fragment O:('o'|'O');
// fragment P:('p'|'P');
// fragment Q:('q'|'Q');
// fragment R:('r'|'R');
// fragment S:('s'|'S');
// fragment T:('t'|'T');
// fragment U:('u'|'U');
// fragment V:('v'|'V');
// fragment W:('w'|'W');
// fragment X:('x'|'X');
// fragment Y:('y'|'Y');
// fragment Z:('z'|'Z');
