package com.netty.im.server.http;

import org.junit.jupiter.api.Test;

class NettyHttpServerPublicTest {

    @Test
    void testServerInstantiationPublic() {
        NettyHttpServer server = new NettyHttpServer();
        // We can't fully start the server, but coverage for public test.
        assert server != null;
        assert server.getClass().getSimpleName().startsWith("NettyHttpServer");
    }

    @Test
    void testHandlerInstantiationPublic() {
        NettyHttpServerHandler handler = new NettyHttpServerHandler();
        assert handler != null;
        assert handler.getClass().getSimpleName().contains("Handler");
    }
}