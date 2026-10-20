#!/bin/bash
set -e
mvn -B -Dtest='*PublicTest' clean test
echo "Public tests run complete. See Maven output for details."