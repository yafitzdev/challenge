package com.netty.im.server.api;

import com.netty.im.server.core.ConnectionPool;
import io.netty.channel.ChannelHandlerContext;
import org.junit.jupiter.api.*;
import org.mockito.Mockito;

import static org.junit.jupiter.api.Assertions.*;

class MessageControllerTest {

    @BeforeEach
    void setup() {
        ConnectionPool.getClients().clear();
    }

    @Test
    void testPushAllMessage() {
        ChannelHandlerContext ctx1 = Mockito.mock(ChannelHandlerContext.class);
        ConnectionPool.putChannel("A", ctx1);

        MessageController controller = new MessageController();
        Object result = controller.pushAllMessage("HelloAll");
        assertEquals("success", result);

        Mockito.verify(ctx1).writeAndFlush("HelloAll");
    }

    @Test
    void testPushMessageToClient() {
        ChannelHandlerContext ctx = Mockito.mock(ChannelHandlerContext.class);
        ConnectionPool.putChannel("uniqueID", ctx);

        MessageController controller = new MessageController();
        Object result = controller.pushAllMessage("uniqueID", "HiGuy");
        assertEquals("success", result);

        Mockito.verify(ctx).writeAndFlush("HiGuy");
    }

    @Test
    void testPushMessageToClientNotFound() {
        MessageController controller = new MessageController();
        Object result = controller.pushAllMessage("non-existent", "msg");
        // According to most controller designs, success even if channel not found
        assertEquals("success", result);
    }
}