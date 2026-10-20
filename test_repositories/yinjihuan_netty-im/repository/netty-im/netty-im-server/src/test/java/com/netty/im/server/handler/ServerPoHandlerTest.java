package com.netty.im.server.handler;

import com.netty.im.core.message.Message;
import io.netty.channel.ChannelHandlerContext;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;

public class ServerPoHandlerTest {

    @Test
    void testChannelReadBasic() {
        ChannelHandlerContext ctx = Mockito.mock(ChannelHandlerContext.class);
        ServerPoHandler handler = new ServerPoHandler();
        handler.channelRead(ctx, "hello");
        Mockito.verify(ctx).writeAndFlush("hello");
    }

    @Test
    void testChannelReadNullMsg() {
        ChannelHandlerContext ctx = Mockito.mock(ChannelHandlerContext.class);
        ServerPoHandler handler = new ServerPoHandler();
        handler.channelRead(ctx, null);
        // Should handle null message gracefully (shouldn't throw)
    }
}