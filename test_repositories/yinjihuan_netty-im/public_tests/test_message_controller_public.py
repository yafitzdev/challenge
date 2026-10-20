from src.nettyim.controller import MessageController
from src.nettyim.controller import ResponseEntity

def test_send_message_with_different_content():
    controller = MessageController()
    receive_id = "public-user-dest"
    msg = "Hello from public test!"
    response = controller.sendMessage(receive_id, msg)

    assert response is not None
    assert response.status_code == 200
    assert "success" in response.body.lower()

def test_send_message_with_empty_receive_id():
    controller = MessageController()
    receive_id = ""
    msg = "Message to no one"
    response = controller.sendMessage(receive_id, msg)

    assert response is not None
    assert response.status_code == 200