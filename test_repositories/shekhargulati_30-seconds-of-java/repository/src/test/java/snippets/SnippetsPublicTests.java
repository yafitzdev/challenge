package snippets;

import org.junit.Test;

import java.util.OptionalInt;

import static org.assertj.core.api.Assertions.assertThat;

public class SnippetsPublicTests {

    @Test
    public void gcd_of_array_containing_6_9_15_is_3() throws Exception {
        OptionalInt gcd = Snippets.gcd(new int[]{6, 9, 15});
        assertThat(gcd).isNotEmpty();
        assertThat(gcd).hasValue(3);
    }

    @Test
    public void gcd_of_array_containing_14_28_56_is_14() throws Exception {
        OptionalInt gcd = Snippets.gcd(new int[]{14, 28, 56});
        assertThat(gcd).isNotEmpty();
        assertThat(gcd).hasValue(14);
    }

    @Test
    public void lcm_of_array_containing_2_3_7_is_42() throws Exception {
        OptionalInt lcm = Snippets.lcm(new int[]{2, 3, 7});
        assertThat(lcm).isNotEmpty();
        assertThat(lcm).hasValue(42);
    }

    @Test
    public void lcm_of_array_containing_5_10_20_is_20() throws Exception {
        OptionalInt lcm = Snippets.lcm(new int[]{5, 10, 20});
        assertThat(lcm).isNotEmpty();
        assertThat(lcm).hasValue(20);
    }

    @Test
    public void max_of_array_containing_4_8_and_6_is_8() throws Exception {
        OptionalInt max = Snippets.arrayMax(new int[]{4, 8, 6});
        assertThat(max).hasValue(8);
    }

    @Test
    public void min_of_array_containing_17_8_and_25_is_8() throws Exception {
        OptionalInt min = Snippets.arrayMin(new int[]{17, 8, 25});
        assertThat(min).hasValue(8);
    }

    @Test
    public void chunk_breaks_input_array_with_size_3() throws Exception {
        int[][] chunks = Snippets.chunk(new int[]{10, 20, 30, 40, 50, 60, 70}, 3);
        assertThat(chunks)
                .containsExactly(
                        new int[]{10, 20, 30},
                        new int[]{40, 50, 60},
                        new int[]{70}
                );
    }

    @Test
    public void chunk_breaks_input_array_evenly_with_size_4() throws Exception {
        int[][] chunks = Snippets.chunk(new int[]{2, 4, 6, 8, 10, 12, 14, 16}, 4);
        assertThat(chunks)
                .containsExactly(
                        new int[]{2, 4, 6, 8},
                        new int[]{10, 12, 14, 16}
                );
    }

    @Test
    public void countOccurrences_counts_occurrences_of_value_5() throws Exception {
        long count = Snippets.countOccurrences(new int[]{5, 3, 5, 2, 5, 6}, 5);
        assertThat(count).isEqualTo(3);
    }

    @Test
    public void deepFlatten_flattens_varied_nested_array() throws Exception {
        int[] flatten = Snippets.deepFlatten(
                new Object[]{7, new Object[]{8, new Object[]{9, 10}}, 11}
        );
        assertThat(flatten).isEqualTo(new int[]{7, 8, 9, 10, 11});
    }

    @Test
    public void difference_between_array_9_8_7_and_7_8_5_is_9() throws Exception {
        int[] difference = Snippets.difference(new int[]{9, 8, 7}, new int[]{7, 8, 5});
        assertThat(difference).isEqualTo(new int[]{9});
    }

    // ... Additional public tests for other methods can be added here as necessary,
    // making sure to use different input/output data than original tests.

}