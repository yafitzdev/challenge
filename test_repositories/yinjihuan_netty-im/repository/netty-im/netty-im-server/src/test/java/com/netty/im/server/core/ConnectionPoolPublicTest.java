package com.netty.im.server.core;

import io.netty.channel.ChannelHandlerContext;
import org.junit.jupiter.api.*;
import org.mockito.Mockito;

import java.util.List;
import java.util.Set;

import static org.junit.jupiter.api.Assertions.*;

class ConnectionPoolPublicTest {

    @BeforeEach
    void cleanPool() {
        ConnectionPool.getClients().clear();
    }

    @Test
    void testPutAndGetChannelWithDifferentId() {
        ChannelHandlerContext ctx = Mockito.mock(ChannelHandlerContext.class);
        assertNull(ConnectionPool.getChannel("public_id"));
        ConnectionPool.putChannel("publicUserA", ctx);
        assertEquals(ctx, ConnectionPool.getChannel("publicUserA"));
    }

    @Test
    void testPutChannelReturnsOldValuePublic() {
        ChannelHandlerContext ctx1 = Mockito.mock(ChannelHandlerContext.class);
        ChannelHandlerContext ctx2 = Mockito.mock(ChannelHandlerContext.class);
        assertNull(ConnectionPool.putChannel("publicClient", ctx1));
        assertEquals(ctx1, ConnectionPool.putChannel("publicClient", ctx2));
        assertEquals(ctx2, ConnectionPool.getChannel("publicClient"));
    }

    @Test
    void testGetChannelNullClientIdPublic() {
        assertNull(ConnectionPool.getChannel(null));
    }

    @Test
    void testGetClientsPublic() {
        ChannelHandlerContext ctx = Mockito.mock(ChannelHandlerContext.class);
        ConnectionPool.putChannel("alice", ctx);
        Set<String> clients = ConnectionPool.getClients();
        assertTrue(clients.contains("alice"));
        assertFalse(clients.contains("bob"));
        assertNotNull(clients);
    }

    @Test
    void testGetChannelsPublic() {
        ChannelHandlerContext ctx4 = Mockito.mock(ChannelHandlerContext.class);
        ConnectionPool.putChannel("publicFour", ctx4);
        List<ChannelHandlerContext> channels = ConnectionPool.getChannels();
        assertTrue(channels.contains(ctx4));
        assertEquals(ConnectionPool.getClients().size(), channels.size());
    }

    @Test
    void testPutChannelNullClientIdPublic() {
        ChannelHandlerContext ctx = Mockito.mock(ChannelHandlerContext.class);
        assertNull(ConnectionPool.putChannel(null, ctx));
    }
}