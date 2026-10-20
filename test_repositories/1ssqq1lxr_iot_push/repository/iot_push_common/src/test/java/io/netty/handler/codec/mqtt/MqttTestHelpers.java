// Stub test helpers for netty-mqtt classes if needed for basic instantiation
package io.netty.handler.codec.mqtt;

public class MqttTestHelpers {
    public static MqttFixedHeader createMqttFixedHeader() {
        return new MqttFixedHeader(MqttMessageType.CONNECT, false, MqttQoS.AT_LEAST_ONCE, false, 1);
    }
}