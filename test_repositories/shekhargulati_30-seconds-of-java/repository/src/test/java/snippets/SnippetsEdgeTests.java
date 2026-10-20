package snippets;

import org.junit.Test;

import static org.assertj.core.api.Assertions.assertThat;

public class SnippetsEdgeTests {

    @Test
    public void gcd_with_array_of_zeros_is_zero() throws Exception {
        assertThat(Snippets.gcd(new int[]{0, 0, 0})).hasValue(0);
    }

    @Test
    public void lcm_with_single_element_array_is_value_itself() throws Exception {
        assertThat(Snippets.lcm(new int[]{42})).hasValue(42);
    }

    @Test
    public void arrayMax_with_negative_numbers_returns_max() throws Exception {
        assertThat(Snippets.arrayMax(new int[]{-5, -1, -12})).hasValue(-1);
    }

    @Test
    public void arrayMin_with_all_equal_numbers_returns_that_number() throws Exception {
        assertThat(Snippets.arrayMin(new int[]{3, 3, 3})).hasValue(3);
    }

    @Test
    public void chunk_empty_array_returns_empty_result() throws Exception {
        int[][] chunks = Snippets.chunk(new int[]{}, 3);
        assertThat(chunks).isEmpty();
    }

    @Test
    public void countOccurrences_no_matching_values_returns_zero() throws Exception {
        assertThat(Snippets.countOccurrences(new int[]{7, 8, 9}, 5)).isEqualTo(0L);
    }

    @Test
    public void deepFlatten_empty_array_returns_empty_array() throws Exception {
        int[] flatten = Snippets.deepFlatten(new Object[]{});
        assertThat(flatten).isEmpty();
    }

    @Test
    public void difference_with_first_array_empty_returns_empty() throws Exception {
        int[] difference = Snippets.difference(new int[]{}, new int[]{1, 2});
        assertThat(difference).isEmpty();
    }

    @Test
    public void difference_with_second_array_empty_returns_first_array() throws Exception {
        int[] difference = Snippets.difference(new int[]{2, 3, 4}, new int[]{});
        assertThat(difference).isEqualTo(new int[]{2, 3, 4});
    }

    // Additional edge tests as necessary.
}