#!/bin/bash
cd iot_push_common
mvn -Dtest='*PublicTest' test
cd ..