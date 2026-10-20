import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TimeAdditionalPublicTest {

    @Test
    public void testTimeToSecondsAndConversion() {
        ch11.Time t = new ch11.Time(6, 4, 15.0);
        double seconds = ch11.Time.timeToSeconds(t);
        assertEquals(6*3600 + 4*60 + 15.0, seconds, 1e-8);

        ch11.Time t2 = ch11.Time.secondsToTime(3678.5);
        assertEquals(1, getField(t2, "hour"));
        assertEquals(1, getField(t2, "minute"));
        assertEquals(18.5, getDoubleField(t2, "second"), 1e-8);
    }

    @Test
    public void testSubtractTime() {
        ch11.Time t1 = new ch11.Time(7, 10, 15.0);
        ch11.Time t2 = new ch11.Time(4, 20, 15.0);
        ch11.Time diff = ch11.Time.subtract(t1, t2);
        assertEquals(2, getField(diff, "hour"));
        assertEquals(50, getField(diff, "minute"));
        assertEquals(0.0, getDoubleField(diff, "second"), 1e-8);
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