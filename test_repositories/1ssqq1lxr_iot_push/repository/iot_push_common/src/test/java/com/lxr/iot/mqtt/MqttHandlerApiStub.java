package com.lxr.iot.mqtt;

import io.netty.channel.Channel;
import io.netty.handler.codec.mqtt.MqttMessage;
import io.netty.handler.timeout.IdleStateEvent;

public class MqttHandlerApiStub implements MqttHandlerIntf {
    public boolean closed = false;
    public boolean doTimeoutCalled = false;

    @Override
    public void close(Channel channel) {
        closed = true;
    }
    @Override
    public void puback(Channel channel, MqttMessage mqttMessage) { }
    @Override
    public void pubrec(Channel channel, MqttMessage mqttMessage) { }
    @Override
    public void pubrel(Channel channel, MqttMessage mqttMessage) { }
    @Override
    public void pubcomp(Channel channel, MqttMessage mqttMessage) { }
    @Override
    public void doTimeOut(Channel channel, IdleStateEvent evt) {
        doTimeoutCalled = true;
    }
}