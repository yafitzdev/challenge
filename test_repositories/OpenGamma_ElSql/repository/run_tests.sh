#!/bin/bash
set -e
mvn -B clean test jacoco:report
echo "Tests and coverage report complete. See target/site/jacoco/index.html"