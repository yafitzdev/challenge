#!/bin/bash
# Use JAVA_HOME override for gradle to fix Java 17 compatibility issues
export JAVA_HOME=$(dirname $(dirname $(readlink -f $(which javac))))
cd contacts
../gradlew test --tests '*PublicTest'