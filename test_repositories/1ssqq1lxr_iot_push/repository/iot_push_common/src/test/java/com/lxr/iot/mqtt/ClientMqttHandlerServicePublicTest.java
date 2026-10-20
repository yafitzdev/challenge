package com.lxr.iot.mqtt;

import org.junit.Test;

import static org.junit.Assert.*;

public class ClientMqttHandlerServicePublicTest {
    @Test
    public void testClientMqttHandlerPublicConstruction() {
        // Different logic: test via an anonymous subclass since ClientMqttHandlerService is abstract.
        ClientMqttHandlerService client = new ClientMqttHandlerService() {
            @Override public void heart(io.netty.channel.Channel ch, io.netty.handler.timeout.IdleStateEvent evt) {}
            @Override public void suback(io.netty.channel.Channel ch, io.netty.handler.codec.mqtt.MqttSubAckMessage msg) {}
            @Override public void pubBackMessage(io.netty.channel.Channel ch, int i) {}
            @Override public void unsubBack(io.netty.channel.Channel ch, io.netty.handler.codec.mqtt.MqttMessage msg) {}
        };
        assertNotNull(client);
    }
}