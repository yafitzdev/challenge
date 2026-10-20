#!/bin/bash
# Run only public tests from the library module for SmsRadar, using Maven.
# This will restrict test execution to *PublicTest.java (and SmsTestPublicTest.java).
cd library
mvn -Dtest=**/*PublicTest test