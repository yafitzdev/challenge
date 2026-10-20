#!/bin/bash
set -e

# Run all tests using Maven and generate coverage report
mvn test jacoco:report