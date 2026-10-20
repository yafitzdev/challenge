#!/bin/bash
# Runs all tests (including non-public) for both modules

./gradlew --no-daemon -p dyno-queues-core test
if [ $? -ne 0 ]; then
  echo "Core tests failed"
  exit 1
fi

./gradlew --no-daemon -p dyno-queues-redis test
if [ $? -ne 0 ]; then
  echo "Redis tests failed"
  exit 1
fi