#!/bin/bash
set -e

# Run only public tests using Maven's includes filter.
mvn -Dtest='*PublicTest' test