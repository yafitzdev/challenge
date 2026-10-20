package com.netty.im.server.handler;

import org.junit.jupiter.api.Test;

class ServerPoHandlerPublicTest {

    @Test
    void testServerPoHandlerConstructionPublic() {
        ServerPoHandler handler = new ServerPoHandler();
        assert handler != null;
        assert handler.getClass().getSimpleName().equals("ServerPoHandler");
    }

    @Test
    void testServerPoHandlerProtoConstructionPublic() {
        ServerPoHandlerProto handlerProto = new ServerPoHandlerProto();
        assert handlerProto != null;
        assert handlerProto.getClass().getSimpleName().contains("Proto");
    }

    @Test
    void testServerStringHandlerConstructionPublic() {
        ServerStringHandler stringHandler = new ServerStringHandler();
        assert stringHandler != null;
        assert stringHandler.getClass().getSimpleName().contains("String");
    }
}