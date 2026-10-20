#!/bin/bash
cd "$(dirname "$0")"
mvn clean test jacoco:report