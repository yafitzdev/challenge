import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TimeClientPublicTest {

    @Test
    public void testCustomToStringPublic() {
        ch11.Time t = new ch11.Time(2, 45, 30.0);
        assertEquals("02:45:30.0\n", t.toString());
    }

    @Test
    public void testAddAndIncrementWithDiffDataPublic() {
        ch11.Time t1 = new ch11.Time(3, 15, 25.0);
        ch11.Time t2 = new ch11.Time(4, 25, 35.0);
        ch11.Time sum = ch11.Time.add(t1, t2);
        assertEquals(7, getField(sum, "hour"));
        assertEquals(40, getField(sum, "minute"));
        assertEquals(60.0, getDoubleField(sum, "second"), 1e-8);

        t1.increment(36.5); // 3:15:25 + 36.5 = 3:16:01.5
        assertEquals("03:16:01.5\n", t1.toString());
    }

    private int getField(ch11.Time t, String name) {
        try {
            java.lang.reflect.Field f = ch11.Time.class.getDeclaredField(name);
            f.setAccessible(true);
            return f.getInt(t);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    private double getDoubleField(ch11.Time t, String name) {
        try {
            java.lang.reflect.Field f = ch11.Time.class.getDeclaredField(name);
            f.setAccessible(true);
            return f.getDouble(t);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }
}