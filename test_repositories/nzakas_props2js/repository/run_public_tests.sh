#!/bin/bash
# Compile the source and public test files using JDK 17 (for class version 61.0)
# Adjust JAVA_HOME if JDK 17 is at a different path in environment

# Set CLASSPATH for JUnit and the local directories for test output.
LIB=./lib
JUNIT=$LIB/junit-4.1.jar
GSON=$LIB/gson-2.0.jar
SRC=./src
TESTS=./tests
OUT=./bin_public

mkdir -p $OUT

# Find all java files in src and public test directories.
find $SRC/net/nczonline/web/props2js/ -name "*.java" > sources.txt
find $TESTS/net/nczonline/web/props2js/ -name "*PublicTest.java" >> sources.txt

# Compile for Java 17
# Use -cp to include junit and gson
javac -cp "$JUNIT:$GSON:$OUT" -d $OUT @sources.txt

# Run each public test with junit
for test in $(find $TESTS/net/nczonline/web/props2js/ -name "*PublicTest.java")
do
    testclass=$(basename $test .java)
    # classes are in package net.nczonline.web.props2js, so need fully qualified names
    fqcn="net.nczonline.web.props2js.${testclass}"
    java -cp "$OUT:$JUNIT:$GSON" org.junit.runner.JUnitCore $fqcn
done

rm sources.txt