#!/bin/bash
# Run tests and generate JaCoCo code coverage report

# Ensure JaCoCo is available (download CLI version if not present)
JACOCO_CLI_JAR="lib/jacococli.jar"
if [ ! -f "$JACOCO_CLI_JAR" ]; then
    echo "Downloading JaCoCo CLI JAR..."
    curl -L -o "$JACOCO_CLI_JAR" https://repo1.maven.org/maven2/org/jacoco/org.jacoco.cli/0.8.8/org.jacoco.cli-0.8.8-nodeps.jar
fi

# Create bin directory and compile sources and tests with coverage enabled
mkdir -p bin

# Compile sources
javac -cp "lib/gson-2.0.jar:lib/jargs-1.0.jar:lib/junit-4.1.jar" -d bin $(find src -name "*.java")

# Compile tests
javac -cp "bin:lib/gson-2.0.jar:lib/jargs-1.0.jar:lib/junit-4.1.jar" -d bin $(find tests -name "*.java")

# Remove previous coverage data
rm -f jacoco.exec

# Run tests with JaCoCo agent
java -javaagent:lib/jacocoagent.jar=destfile=jacoco.exec -cp "bin:lib/gson-2.0.jar:lib/jargs-1.0.jar:lib/junit-4.1.jar" org.junit.runner.JUnitCore net.nczonline.web.props2js.PropertyConverterTest

# Generate HTML coverage report
mkdir -p coverage
java -jar $JACOCO_CLI_JAR report jacoco.exec --classfiles bin --sourcefiles src --html coverage

echo "Coverage report generated in coverage/index.html"