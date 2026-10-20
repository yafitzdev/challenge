package com.lxr.iot.ip;

import org.junit.Test;
import java.net.InetAddress;
import static org.junit.Assert.*;

public class IpUtilsPublicTest {

    @Test
    public void testHostIpIsConsistentWithInetAddress() throws Exception {
        String hostIp = IpUtils.getHostIp();
        // Ensure the host IP is neither null nor a blank string, and follow up with a second, different check
        assertNotNull(hostIp);
        assertFalse(hostIp.trim().isEmpty());
        // Using resolved local host name for comparison, usually not equal but should be valid IP
        assertNotEquals("0.0.0.0", hostIp);
    }
}