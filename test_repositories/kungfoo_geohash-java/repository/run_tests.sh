#!/bin/bash
# Runs all Java tests for the kungfoo_geohash-java project using Maven.

set -e

# Ensure mvn is installed
if ! command -v mvn &> /dev/null
then
    echo "Maven (mvn) could not be found. Please install Maven to proceed."
    exit 1
fi

mvn test