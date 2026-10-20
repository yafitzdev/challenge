#!/bin/bash
# Run only the public test files (those ending in PublicTest.java)
./gradlew :Application:test --tests '*PublicTest'