import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TimeTest {

    @Test
    public void testDefaultConstructor() {
        Time t = new Time();
        assertEquals("00:00:00.0\n", t.toString());
    }

    @Test
    public void testParameterizedConstructorAndToString() {
        Time t = new Time(9, 15, 7.7);
        assertEquals("09:15:07.7\n", t.toString());
    }

    @Test
    public void testEqualsTrueAndFalse() {
        Time t1 = new Time(2, 5, 10.0);
        Time t2 = new Time(2, 5, 10.0);
        Time t3 = new Time(3, 5, 10.0);
        assertTrue(t1.equals(t2));
        assertFalse(t1.equals(t3));
    }

    @Test
    public void testAddStatic() {
        Time t1 = new Time(1, 20, 30.0);
        Time t2 = new Time(2, 40, 15.5);
        Time sum = Time.add(t1, t2);
        assertEquals("03:60:45.5\n", sum.toString());
    }

    @Test
    public void testAddInstanceNoRollover() {
        Time t1 = new Time(1, 20, 10.0);
        Time t2 = new Time(2, 10, 30.0);
        Time sum = t1.add(t2);
        assertEquals("03:30:40.0\n", sum.toString());
    }

    @Test
    public void testAddInstanceWithSecondRollover() {
        Time t1 = new Time(1, 50, 40.0);
        Time t2 = new Time(0, 5, 25.0);
        Time sum = t1.add(t2);
        // 40+25=65, so 65-60=5 sec, minute +1: 50+5+1=56
        assertEquals("01:56:05.0\n", sum.toString());
    }

    @Test
    public void testAddInstanceWithMinuteRollover() {
        Time t1 = new Time(1, 55, 50.0);
        Time t2 = new Time(0, 6, 15.0);
        Time sum = t1.add(t2);
        // 50+15=65, so 65-60=5, minute+1: 55+6+1=62, 62-60=2-minutes, hour+1: 1+0+1=2
        assertEquals("02:02:05.0\n", sum.toString());
    }

    @Test
    public void testIncrementNoRollover() {
        Time t = new Time(2, 15, 50.0);
        t.increment(5.5);
        assertEquals("02:15:55.5\n", t.toString());
    }

    @Test
    public void testIncrementSecondsToMinuteRollover() {
        Time t = new Time(0, 44, 50.0);
        t.increment(14.0); // 64.0 sec => 4.0 sec and +1 min
        assertEquals("00:45:04.0\n", t.toString());
    }

    @Test
    public void testIncrementSecondsAndMinuteRollover() {
        Time t = new Time(1, 59, 55.0);
        t.increment(10.0); // 65.0 sec => 5.0 sec and +1 min; minute 59+1=60 => 0 +1hr
        assertEquals("02:00:05.0\n", t.toString());
    }
}