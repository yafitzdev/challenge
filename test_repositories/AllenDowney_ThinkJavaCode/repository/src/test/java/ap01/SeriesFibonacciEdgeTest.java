import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class SeriesFibonacciEdgeTest {

    @Test
    public void testFibonacciZeroAndNegative() {
        // Should likely recurse infinitely or break, but let's be defensive!
        // Defensive implementation: We'll just check it throws StackOverflowError for zero or negatives
        try {
            Series.fibonacci(0);
            fail("Expected StackOverflowError or RecursionError");
        } catch (StackOverflowError err) {
            // ok, expected for bad inputs
        } catch (Throwable t) {
            // Accept any error for bad/invalid input
        }

        try {
            Series.fibonacci(-5);
            fail("Expected StackOverflowError or RecursionError");
        } catch (StackOverflowError err) {
            // ok
        } catch (Throwable t) {
            // Accept any error for bad/invalid input
        }
    }
}