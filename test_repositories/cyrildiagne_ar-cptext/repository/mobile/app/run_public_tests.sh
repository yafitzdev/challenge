#!/bin/bash
# Runs only public test classes (those named *PublicTest.java)
./gradlew --no-daemon test --tests '*PublicTest'