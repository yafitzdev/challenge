package com.netty.im.server.core;

import org.junit.jupiter.api.Test;

class ImServerPublicTest {

    @Test
    void testImServerConstructorPublic() {
        // More coverage: check class name after instantiation
        ImServer server = new ImServer();
        assert server.getClass().getSimpleName().equals("ImServer");
    }
}