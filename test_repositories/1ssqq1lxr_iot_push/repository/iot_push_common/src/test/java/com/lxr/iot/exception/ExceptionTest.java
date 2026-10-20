package com.lxr.iot.exception;

import org.junit.Test;

public class ExceptionTest {

    @Test(expected = ConnectionException.class)
    public void testConnectionExceptionThrow() throws Throwable {
        throw new ConnectionException("Connection error");
    }

    @Test(expected = NoFindHandlerException.class)
    public void testNoFindHandlerExceptionThrow() throws Throwable {
        throw new NoFindHandlerException("No handler found");
    }
}