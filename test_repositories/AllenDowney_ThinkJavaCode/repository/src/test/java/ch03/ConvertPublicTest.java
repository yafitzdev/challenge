import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class ConvertPublicTest {

    @Test
    public void testCelsiusToFahrenheitPublicData() {
        // 0C = 32F, 50C = 122F, 20C = 68F, 37C = 98.6F
        assertEquals(32.0, ch03.Convert.celsiusToFahrenheit(0), 0.01);
        assertEquals(122.0, ch03.Convert.celsiusToFahrenheit(50), 0.01);
        assertEquals(68.0, ch03.Convert.celsiusToFahrenheit(20), 0.01);
        assertEquals(98.6, ch03.Convert.celsiusToFahrenheit(37), 0.01);
    }

    @Test
    public void testFahrenheitToCelsiusPublicData() {
        // 32F=0C, 212F=100C, 104F=40C, 41F=5C
        assertEquals(0.0, ch03.Convert.fahrenheitToCelsius(32), 0.01);
        assertEquals(100.0, ch03.Convert.fahrenheitToCelsius(212), 0.01);
        assertEquals(40.0, ch03.Convert.fahrenheitToCelsius(104), 0.01);
        assertEquals(5.0, ch03.Convert.fahrenheitToCelsius(41), 0.01);
    }
}