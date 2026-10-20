// Dummy stub (simplified) for Netty EmbeddedChannel for test environments that lack Netty test classes
package io.netty.channel;

import io.netty.channel.ChannelHandler;

public class EmbeddedChannel extends AbstractChannel {
    private final ChannelHandler handler;
    public EmbeddedChannel(ChannelHandler handler) {
        super(null);
        this.handler = handler;
    }
    @Override
    protected AbstractUnsafe newUnsafe() {return null;}
    @Override
    protected boolean isCompatible(EventLoop loop) {return true;}
    @Override
    protected void doBind(java.net.SocketAddress localAddress) throws Exception {}
    @Override
    protected void doDisconnect() throws Exception {}
    @Override
    protected void doClose() throws Exception {
        ((MqttHandlerApiStub) handler).close(this);
    }
    @Override
    protected void doBeginRead() throws Exception {}
    @Override
    protected void doWrite(java.util.List<Object> msgs) throws Exception {}
    @Override
    public ChannelConfig config() {return null;}
    @Override
    public boolean isOpen() {return true;}
    @Override
    public boolean isActive() {return true;}
    @Override
    public java.net.SocketAddress localAddress() {return null;}
    @Override
    public java.net.SocketAddress remoteAddress() {return null;}
    @Override
    public Channel parent() {return null;}
}