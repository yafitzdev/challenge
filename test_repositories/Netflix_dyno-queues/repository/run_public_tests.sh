#!/bin/bash
# Runs only public tests (those with PublicTest in the name) for both modules

./gradlew --no-daemon -p dyno-queues-core test --tests '*PublicTest'
if [ $? -ne 0 ]; then
  echo "Core public tests failed"
  exit 1
fi

./gradlew --no-daemon -p dyno-queues-redis test --tests '*PublicTest'
if [ $? -ne 0 ]; then
  echo "Redis public tests failed"
  exit 1
fi