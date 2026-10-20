package com.lxr.iot.mqtt;

import org.junit.Test;

import static org.junit.Assert.*;

public class ServerMqttHandlerServicePublicTest {
    @Test
    public void testServerMqttHandlerNewConstruction() {
        // Use anonymous subclass since ServerMqttHandlerService may be abstract or complex in impl
        ServerMqttHandlerService server = new ServerMqttHandlerService() {};
        assertNotNull(server);
    }
}