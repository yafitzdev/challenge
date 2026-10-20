package com.lxr.iot.properties;

import org.junit.Test;
import static org.junit.Assert.*;

public class PropertiesTest {
    @Test
    public void testMqttProperties() {
        MqttProperties props = new MqttProperties();
        props.setPort(1883);
        props.setHost("127.0.0.1");
        props.setClientId("cid");
        props.setUsername("user");
        props.setPassword("pass");
        props.setCleanSession(true);
        props.setKeepalive(120);
        props.setQos(1);

        assertEquals(1883, props.getPort());
        assertEquals("127.0.0.1", props.getHost());
        assertEquals("cid", props.getClientId());
        assertEquals("user", props.getUsername());
        assertEquals("pass", props.getPassword());
        assertTrue(props.isCleanSession());
        assertEquals(120, props.getKeepalive());
        assertEquals(1, props.getQos());
    }
}