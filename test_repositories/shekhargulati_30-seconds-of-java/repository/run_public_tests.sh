#!/bin/bash
# Script to run all public tests for shekhargulati_30-seconds-of-java

# Exit immediately if a command exits with a non-zero status
set -e

echo "Running public tests using Maven..."

# Run ONLY tests with class names ending with 'PublicTests'
./mvnw -Dtest='*PublicTests' test