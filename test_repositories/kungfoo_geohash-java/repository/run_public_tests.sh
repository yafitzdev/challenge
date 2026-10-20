#!/bin/bash
# Runs all public Java tests (files named *PublicTest.java) for the kungfoo_geohash-java project using Maven.

set -e

# Compile all *PublicTest.java files and run them via surefire
if ! command -v mvn &> /dev/null
then
    echo "Maven (mvn) could not be found. Please install Maven to proceed."
    exit 1
fi

# Run only tests in files with PublicTest in the name
mvn -Dtest='*PublicTest' test