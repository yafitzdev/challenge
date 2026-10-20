#!/bin/bash
cd "$(dirname "$0")"
./mvnw test -Dtest="com.example.GreeterPublicTest"