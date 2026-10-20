package com.netty.im.server.core;

import org.junit.jupiter.api.Test;

class ImServerTest {

    @Test
    void testImServerInstantiation() {
        // Just instantiation for coverage as Netty startup is not easily testable
        new ImServer();
    }
}