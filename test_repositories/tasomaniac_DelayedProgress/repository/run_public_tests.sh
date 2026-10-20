#!/bin/bash
# Force Java 8 for compatibility and run only public tests
export JAVA_HOME=$(/usr/libexec/java_home -v 1.8 2>/dev/null || /usr/lib/jvm/java-8-openjdk-amd64)
export PATH=$JAVA_HOME/bin:$PATH
./gradlew clean test --tests '*PublicTest' --no-daemon