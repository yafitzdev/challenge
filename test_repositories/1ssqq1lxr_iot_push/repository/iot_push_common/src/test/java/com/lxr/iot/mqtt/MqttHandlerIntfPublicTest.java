package com.lxr.iot.mqtt;

import org.junit.Test;

public class MqttHandlerIntfPublicTest {
    @Test
    public void testInterfacePublicImpl() {
        // Provide a different dummy implementation class name
        class PublicDummyMqttHandler implements MqttHandlerIntf {}
        new PublicDummyMqttHandler();
    }
}