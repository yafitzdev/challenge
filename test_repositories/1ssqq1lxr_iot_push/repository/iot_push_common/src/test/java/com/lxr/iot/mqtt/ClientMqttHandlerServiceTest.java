package com.lxr.iot.mqtt;

import org.junit.Test;

import static org.junit.Assert.*;

public class ClientMqttHandlerServiceTest {
    @Test
    public void testClientMqttHandlerConstruction() {
        ClientMqttHandlerService client = new ClientMqttHandlerService();
        assertNotNull(client);
    }
}