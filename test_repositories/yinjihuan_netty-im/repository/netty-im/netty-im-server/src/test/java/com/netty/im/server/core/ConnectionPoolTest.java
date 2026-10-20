package com.netty.im.server.core;

import io.netty.channel.ChannelHandlerContext;
import org.junit.jupiter.api.*;
import org.mockito.Mockito;

import java.util.List;
import java.util.Set;

import static org.junit.jupiter.api.Assertions.*;

class ConnectionPoolTest {

    @BeforeEach
    void clearPool() {
        // Clean: directly clear underlying storage using reflection if needed
        ConnectionPool.getClients().clear();
    }

    @Test
    void testPutAndGetChannel() {
        ChannelHandlerContext ctx = Mockito.mock(ChannelHandlerContext.class);
        assertNull(ConnectionPool.getChannel("non_existent"));
        ConnectionPool.putChannel("client1", ctx);
        assertEquals(ctx, ConnectionPool.getChannel("client1"));
    }

    @Test
    void testPutChannelReturnsOldValue() {
        ChannelHandlerContext ctx1 = Mockito.mock(ChannelHandlerContext.class);
        ChannelHandlerContext ctx2 = Mockito.mock(ChannelHandlerContext.class);
        assertNull(ConnectionPool.putChannel("client2", ctx1));
        assertEquals(ctx1, ConnectionPool.putChannel("client2", ctx2));
        assertEquals(ctx2, ConnectionPool.getChannel("client2"));
    }

    @Test
    void testGetChannelNullClientId() {
        assertNull(ConnectionPool.getChannel(null));
    }

    @Test
    void testGetClients() {
        ChannelHandlerContext ctx = Mockito.mock(ChannelHandlerContext.class);
        ConnectionPool.putChannel("cc", ctx);
        Set<String> clients = ConnectionPool.getClients();
        assertTrue(clients.contains("cc"));
        assertNotNull(clients);
    }

    @Test
    void testGetChannels() {
        ChannelHandlerContext ctx3 = Mockito.mock(ChannelHandlerContext.class);
        ConnectionPool.putChannel("client3", ctx3);
        List<ChannelHandlerContext> channels = ConnectionPool.getChannels();
        assertTrue(channels.contains(ctx3));
    }

    @Test
    void testPutChannelNullClientId() {
        ChannelHandlerContext ctx = Mockito.mock(ChannelHandlerContext.class);
        assertNull(ConnectionPool.putChannel(null, ctx));
    }
}