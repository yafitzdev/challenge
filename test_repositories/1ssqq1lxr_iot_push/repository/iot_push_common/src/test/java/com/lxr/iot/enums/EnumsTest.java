package com.lxr.iot.enums;

import org.junit.Test;
import static org.junit.Assert.*;

public class EnumsTest {

    @Test
    public void testConfirmStatusEnum() {
        assertEquals(2, ConfirmStatus.values().length);
        assertEquals(ConfirmStatus.PUBLISH, ConfirmStatus.valueOf("PUBLISH"));
        assertEquals(ConfirmStatus.PUBREL, ConfirmStatus.valueOf("PUBREL"));
    }

    @Test
    public void testProtocolEnum() {
        assertEquals(2, ProtocolEnum.values().length);
        assertEquals(ProtocolEnum.MQTT, ProtocolEnum.valueOf("MQTT"));
        assertEquals(ProtocolEnum.WEBSOCKET, ProtocolEnum.valueOf("WEBSOCKET"));
    }

    @Test
    public void testQosStatus() {
        assertEquals(3, QosStatus.values().length);
        assertEquals(QosStatus.QOS0, QosStatus.valueOf("QOS0"));
        assertEquals(QosStatus.QOS1, QosStatus.valueOf("QOS1"));
        assertEquals(QosStatus.QOS2, QosStatus.valueOf("QOS2"));
        assertEquals(0, QosStatus.QOS0.value());
        assertEquals(1, QosStatus.QOS1.value());
        assertEquals(2, QosStatus.QOS2.value());
    }

    @Test
    public void testSessionStatus() {
        assertEquals(2, SessionStatus.values().length);
        assertEquals(SessionStatus.CLOSE, SessionStatus.valueOf("CLOSE"));
        assertEquals(SessionStatus.OPEN, SessionStatus.valueOf("OPEN"));
    }

    @Test
    public void testSubStatus() {
        assertEquals(2, SubStatus.values().length);
        assertEquals(SubStatus.CANCEL, SubStatus.valueOf("CANCEL"));
        assertEquals(SubStatus.SUBSCRIBE, SubStatus.valueOf("SUBSCRIBE"));
    }
}