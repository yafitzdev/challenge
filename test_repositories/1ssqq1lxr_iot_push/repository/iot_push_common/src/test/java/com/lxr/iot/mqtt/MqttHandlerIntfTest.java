package com.lxr.iot.mqtt;

import org.junit.Test;

public class MqttHandlerIntfTest {
    @Test
    public void testMqttHandlerIntfImpl() {
        // MqttHandlerIntf is interface, simulate minimal usage.
        class DummyMqttHandler implements MqttHandlerIntf {}
        new DummyMqttHandler();
    }
}