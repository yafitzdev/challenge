#!/bin/bash
# Script to run all tests for shekhargulati_30-seconds-of-java

# Exit immediately if a command exits with a non-zero status
set -e

# Provide some output
echo "Running tests using Maven..."

# Execute tests
./mvnw test