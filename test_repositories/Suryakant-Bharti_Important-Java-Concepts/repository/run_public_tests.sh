#!/bin/bash
set -e
# Only run *PublicTest.java files
mvn -Dtest='*PublicTest' test