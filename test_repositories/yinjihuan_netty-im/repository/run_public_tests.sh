#!/bin/bash
# Runs all public tests (test classes with *PublicTest.java) in netty-im-server module
cd netty-im/netty-im-server
if [ -f ./mvnw ]; then
  ./mvnw test -Dtest='**/*PublicTest'
else
  mvn test -Dtest='**/*PublicTest'
fi