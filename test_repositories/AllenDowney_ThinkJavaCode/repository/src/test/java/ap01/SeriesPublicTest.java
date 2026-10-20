import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class SeriesPublicTest {

    @Test
    public void testGeometricSeriesDifferentData() {
        // Testing for a=3, r=2, n=4 → 3 * (2^0 + 2^1 + 2^2 + 2^3) = 3*(1+2+4+8)=3*15=45
        int result = ap01.Series.geometricSeriesSum(3, 2, 4);
        assertEquals(45, result);

        // Testing with a=1, r=10, n=3 → 1*(1+10+100)=111
        assertEquals(111, ap01.Series.geometricSeriesSum(1, 10, 3));
    }

    @Test
    public void testArithmeticSeriesDifferentData() {
        // Testing for a=2, d=5, n=4 → 2+7+12+17=38
        int result = ap01.Series.arithmeticSeriesSum(2, 5, 4);
        assertEquals(38, result);

        // Testing with a=3, d=0, n=5 → 3+3+3+3+3 = 15
        assertEquals(15, ap01.Series.arithmeticSeriesSum(3, 0, 5));
    }
}