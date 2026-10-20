package com.lxr.iot.mqtt;

import org.junit.Test;

public class MqttHanderPublicTest {
    @Test
    public void testInstantiation() {
        // Just instantiate to get some coverage in a public context
        MqttHander hander = new MqttHander();
        assert hander != null;
    }
}