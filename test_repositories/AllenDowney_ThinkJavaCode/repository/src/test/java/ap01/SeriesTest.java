import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class SeriesTest {

    @Test
    public void testFibonacciBaseCases() {
        assertEquals(1, Series.fibonacci(1));
        assertEquals(1, Series.fibonacci(2));
    }

    @Test
    public void testFibonacciSmallN() {
        assertEquals(2, Series.fibonacci(3));
        assertEquals(3, Series.fibonacci(4));
        assertEquals(5, Series.fibonacci(5));
    }

    @Test
    public void testFibonacciLargerN() {
        assertEquals(21, Series.fibonacci(8));
    }
}