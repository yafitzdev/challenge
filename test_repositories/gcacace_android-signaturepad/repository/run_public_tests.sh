#!/bin/bash
# Script to run only public tests for the project from the root directory

cd signature-pad
../gradlew test --tests '*PublicTest'
cd ..