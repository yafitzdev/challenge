package com.lxr.iot.mqtt;

import org.junit.Test;

import static org.junit.Assert.*;

public class ServerMqttHandlerServiceTest {
    @Test
    public void testServerMqttHandlerConstruction() {
        ServerMqttHandlerService server = new ServerMqttHandlerService();
        assertNotNull(server);
    }
}