package com.netty.im.server.api;

import org.junit.jupiter.api.Test;
import org.springframework.http.ResponseEntity;

import static org.junit.jupiter.api.Assertions.*;

class MessageControllerPublicTest {

    @Test
    void testSendMessageWithDifferentContent() {
        MessageController controller = new MessageController();
        String receiveId = "public-user-dest";
        String msg = "Hello from public test!";
        // Use different data than original likely did (see source, not just test)
        ResponseEntity<String> response = controller.sendMessage(receiveId, msg);

        assertNotNull(response);
        assertEquals(200, response.getStatusCodeValue());
        assertTrue(response.getBody().contains("success") || response.getBody().contains("Success"));
    }

    @Test
    void testSendMessageWithEmptyReceiveId() {
        MessageController controller = new MessageController();
        String receiveId = "";
        String msg = "Message to no one";
        ResponseEntity<String> response = controller.sendMessage(receiveId, msg);

        assertNotNull(response);
        assertEquals(200, response.getStatusCodeValue());
    }
}