#!/bin/bash
# Runs only 'PublicTest' classes, skipping any non-public tests
mvn -Dtest='**/*PublicTest.java' test