package com.lxr.iot.ip;

import org.junit.Test;
import java.net.InetAddress;
import static org.junit.Assert.*;

public class IpUtilsTest {

    @Test
    public void testLocalhostAddress() throws Exception {
        String ip = IpUtils.getHostIp();
        assertNotNull(ip);
        assertFalse(ip.isEmpty());
    }
}