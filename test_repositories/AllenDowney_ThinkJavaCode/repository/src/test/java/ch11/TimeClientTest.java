import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class TimeClientTest {

    @Test
    public void smokeTestMain() {
        // Should not throw
        TimeClient.main(new String[] {});
    }
}