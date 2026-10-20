import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TimePublicTest {

    @Test
    public void testToStringAndConstructorPublic() {
        ch11.Time t = new ch11.Time(3, 7, 15.5);
        assertEquals("03:07:15.5\n", t.toString());
    }

    @Test
    public void testAddStaticPublic() {
        ch11.Time t1 = new ch11.Time(5, 10, 10.5);
        ch11.Time t2 = new ch11.Time(6, 20, 50.5);
        ch11.Time sum = ch11.Time.add(t1, t2);
        assertEquals(11, getField(sum, "hour"));
        assertEquals(30, getField(sum, "minute"));
        assertEquals(61.0, getDoubleField(sum, "second"), 1e-8);
    }

    @Test
    public void testAddInstanceWithNoRolloverPublic() {
        ch11.Time t1 = new ch11.Time(2, 10, 20.0);
        ch11.Time t2 = new ch11.Time(2, 40, 25.0);
        ch11.Time sum = t1.add(t2);
        assertEquals("04:50:45.0\n", sum.toString());
    }

    @Test
    public void testIncrementSimplePublic() {
        ch11.Time t = new ch11.Time(1, 2, 3.0);
        t.increment(10.0);
        assertEquals("01:02:13.0\n", t.toString());
    }

    @Test
    public void testIncrementWithMinuteRolloverPublic() {
        ch11.Time t = new ch11.Time(1, 59, 59.0);
        t.increment(2.5);
        assertEquals("02:00:01.5\n", t.toString());
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