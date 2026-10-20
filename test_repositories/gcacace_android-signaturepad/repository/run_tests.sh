#!/bin/bash
# Script to run all existing tests for the project from the root directory

cd signature-pad
../gradlew test
cd ..