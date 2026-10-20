#!/bin/bash
cd iot_push_common
mvn clean test jacoco:report
cd ..