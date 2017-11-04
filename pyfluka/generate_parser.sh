#!/bin/sh

# install the .jar via http://www.antlr.org
java -jar /usr/local/lib/antlr-4.7-complete.jar FlukaLexer.g4 -Dlanguage=Python2 -visitor;
java -jar /usr/local/lib/antlr-4.7-complete.jar FlukaParser.g4 -Dlanguage=Python2 -visitor;
