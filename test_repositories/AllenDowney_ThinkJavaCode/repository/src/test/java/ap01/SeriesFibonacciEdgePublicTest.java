import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class SeriesFibonacciEdgePublicTest {

    @Test
    public void testFibonacciLow() {
        // Test new value n for Fibonacci sequence
        assertEquals(13, ap01.Series.fibonacci(7));
        assertEquals(21, ap01.Series.fibonacci(8));
    }

    @Test
    public void testFibonacciHighDifferentInputs() {
        // Higher index tests, check growth, known fib(12)=144
        assertEquals(55, ap01.Series.fibonacci(10));
        assertEquals(89, ap01.Series.fibonacci(11));
        assertEquals(144, ap01.Series.fibonacci(12));
    }

    @Test
    public void testFibonacciEdge() {
        // Test n=1 and n=2 (both should still work)
        assertEquals(1, ap01.Series.fibonacci(1));
        assertEquals(1, ap01.Series.fibonacci(2));
    }
}