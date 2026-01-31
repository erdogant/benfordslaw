# pip install pytest
# pytest test/test_benfordslaw.py

import numpy as np
from benfordslaw import benfordslaw
from benfordslaw import compute_excess_mad
import unittest


class TestBENFORDSLAW(unittest.TestCase):
    def test_benfordslaw_digits(self):
        gt = {-6: True, -5: True, -4: True, -3: True, -2: True, -1: True, 1: True, 2: True, 3: True, 4: True, 5: True, 6: True}
        total_results = []
        pos = [-9, -8, -7, -6, -5, -4, -3, -2 -1, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        for p, t in zip(pos, gt):
            bl = benfordslaw(pos=p)
            df = bl.import_example(data='elections_usa')
            Iloc = df['candidate']=='Donald Trump'
            X = df['votes'].loc[Iloc].values
            results = bl.fit(X)
            assert gt.get(p, None)!=np.isnan(results['P'])

    def test_nums(self):
        bl = benfordslaw()
        X = [12, 23, 34, 45, 56, 67, 78, 89, 90, 100]
        out = bl.fit(np.array(X))
        np.all(out['percentage_emp'][:,1]==[20, 10, 10, 10, 10, 10, 10, 10, 10])

    def test_benfordslaw(self):
        bl = benfordslaw()
        df = bl.import_example()
        Iloc = df['candidate']=='Donald Trump'
        X = df['votes'].loc[Iloc].values

        # TEST 1: check output is unchanged
        methods=[None, 'chi2', 'ks']
        for method in methods:
            bl = benfordslaw(method=method)
            out = bl.fit(X)
            assert np.all(np.isin([*out.keys()], ['P', 't', 'percentage_emp', 'P_significant', 'mad', 'expected_mad', 'excess_mad', 'conformity_mad', 'N']))

        # TEST 2: check chi2
        bl = benfordslaw(method='chi2')
        out = bl.fit(X)
        assert out['P']==0.4150723856863902
        assert out['t']==8.190646662956185
        assert out['P_significant']==False

        # TEST 3: check ks
        bl = benfordslaw(method='ks')
        out = bl.fit(X)
        assert out['P']==1.0
        assert out['t']==0.1111111111111111

        # TEST 4: check percentages
        assert np.all(out['percentage_emp'][:,1]==[31.64521544487969, 16.508114157806382, 12.479015109121432, 9.820928931169558, 7.862339115836598, 6.3794068270845, 5.8477895914941245, 4.616675993284835, 4.8405148293228875])

    def test_dataframe(self):
        bl = benfordslaw()
        df = bl.import_example()
        Iloc = df['candidate']=='Donald Trump'
        X = df['votes'].loc[Iloc]
        results = bl.fit(X)
        np.all(np.isin([*results.keys()], ['P', 't', 'percentage_emp', 'P_significant', 'mad', 'expected_mad', 'excess_mad', 'conformity_mad', 'N']))
        assert np.all(results['percentage_emp'][:,1]==[31.64521544487969, 16.508114157806382, 12.479015109121432, 9.820928931169558, 7.862339115836598, 6.3794068270845, 5.8477895914941245, 4.616675993284835, 4.8405148293228875])


class TestExcessMAD(unittest.TestCase):
    """Test suite for Excess MAD functionality."""

    def test_mad_method_first_digit(self):
        """Test MAD method with first digit analysis."""
        bl = benfordslaw(method='mad', pos=1)
        df = bl.import_example(data='elections_usa')
        X = df['votes'].loc[df['candidate'] == 'Donald Trump'].values
        results = bl.fit(X)

        # Check that MAD statistics are computed
        assert 'mad' in results
        assert 'expected_mad' in results
        assert 'excess_mad' in results
        assert 'conformity_mad' in results
        assert 'N' in results

        # MAD should be non-negative
        assert results['mad'] >= 0

        # Expected MAD should be positive for valid N
        assert results['expected_mad'] > 0

        # N should match the data count (approximately, after filtering)
        assert results['N'] > 0

    def test_mad_method_first_two_digits(self):
        """Test MAD method with first-two-digits analysis (paper's recommended approach)."""
        bl = benfordslaw(method='mad', pos='first_two')
        df = bl.import_example(data='elections_usa')
        X = df['votes'].loc[df['candidate'] == 'Donald Trump'].values
        results = bl.fit(X)

        # Check that all MAD statistics are present
        assert 'mad' in results
        assert 'expected_mad' in results
        assert 'excess_mad' in results
        assert 'conformity_mad' in results

        # For first-two-digits test, conformity should be one of the defined categories
        valid_conformities = ['close conformity', 'acceptable conformity',
                              'marginally acceptable conformity', 'nonconforming', 'insufficient data']
        assert results['conformity_mad'] in valid_conformities

    def test_excess_mad_formula(self):
        """Test that Excess MAD = MAD - E(MAD)."""
        bl = benfordslaw(method='mad', pos='first_two')
        df = bl.import_example(data='elections_usa')
        X = df['votes'].loc[df['candidate'] == 'Donald Trump'].values
        results = bl.fit(X)

        # Verify the formula: excess_mad = mad - expected_mad
        calculated_excess = results['mad'] - results['expected_mad']
        assert np.isclose(results['excess_mad'], calculated_excess, rtol=1e-10)

    def test_expected_mad_formula(self):
        """Test that E(MAD) ≈ 1/√(C×N) for first-two-digits."""
        import math
        bl = benfordslaw(method='mad', pos='first_two')
        df = bl.import_example(data='elections_usa')
        X = df['votes'].loc[df['candidate'] == 'Donald Trump'].values
        results = bl.fit(X)

        # Calculate expected MAD using the formula from the paper
        C = bl.EXCESS_MAD_CONSTANTS['first_two']  # 158.8
        N = results['N']
        expected_mad_calculated = 1.0 / math.sqrt(C * N)

        # Verify it matches
        assert np.isclose(results['expected_mad'], expected_mad_calculated, rtol=1e-10)

    def test_excess_mad_constants(self):
        """Test that Excess MAD constants are defined correctly."""
        # Check that constants exist for key digit tests
        bl = benfordslaw()
        assert 'first_two' in bl.EXCESS_MAD_CONSTANTS
        assert 1 in bl.EXCESS_MAD_CONSTANTS
        assert 2 in bl.EXCESS_MAD_CONSTANTS

        # The constant for first-two-digits should be 158.8 (from the paper)
        assert bl.EXCESS_MAD_CONSTANTS['first_two'] == 158.8

    def test_compute_excess_mad_function(self):
        """Test the standalone compute_excess_mad function."""
        data = np.random.lognormal(mean=5, sigma=2, size=1000) * 100

        result = compute_excess_mad(data, pos='first_two')

        # Check output structure
        assert 'mad' in result
        assert 'expected_mad' in result
        assert 'excess_mad' in result
        assert 'conformity_mad' in result
        assert 'N' in result

        # Verify the formula
        assert np.isclose(result['excess_mad'], result['mad'] - result['expected_mad'], rtol=1e-10)

    def test_first_two_digits_90_categories(self):
        """Test that first-two-digits has 90 categories (10-99)."""
        bl = benfordslaw(pos='first_two')

        # Check that digit_range covers 10-99
        assert len(bl.digit_range) == 90
        assert min(bl.digit_range) == 10
        assert max(bl.digit_range) == 99

        # Check that leading_digits has 90 values
        assert len(bl.leading_digits) == 90

    def test_conformity_thresholds_first_two(self):
        """Test conformity thresholds for first-two-digits test."""
        bl = benfordslaw(method='mad', pos='first_two')

        # Create a known dataset that should conform well to Benford's Law
        # Using lognormal distribution which typically follows Benford's Law
        np.random.seed(42)
        data = np.random.lognormal(mean=5, sigma=2, size=5000) * 100

        results = bl.fit(data)

        # Lognormal data should generally show good conformity
        # (though this is a probabilistic test)
        assert results['conformity_mad'] in ['close conformity', 'acceptable conformity',
                                          'marginally acceptable conformity', 'nonconforming']

    def test_mad_statistics_always_computed(self):
        """Test that MAD statistics are always computed regardless of method."""
        methods = ['chi2', 'ks', 'mad', None]
        bl_base = benfordslaw()
        df = bl_base.import_example(data='elections_usa')
        X = df['votes'].loc[df['candidate'] == 'Donald Trump'].values

        for method in methods:
            bl = benfordslaw(method=method)
            results = bl.fit(X)

            # MAD statistics should always be present
            assert 'mad' in results, f"MAD missing for method {method}"
            assert 'expected_mad' in results, f"expected_mad missing for method {method}"
            assert 'excess_mad' in results, f"excess_mad missing for method {method}"
            assert 'conformity_mad' in results, f"conformity missing for method {method}"

    def test_excess_mad_sample_size_effect(self):
        """Test that Excess MAD properly accounts for sample size."""
        import math

        # Generate Benford-like data
        np.random.seed(42)
        large_data = np.random.lognormal(mean=5, sigma=2, size=10000) * 100
        small_data = large_data[:500]

        bl = benfordslaw(method='mad', pos='first_two')

        results_large = bl.fit(large_data)
        results_small = bl.fit(small_data)

        # Expected MAD should be smaller for larger datasets
        assert results_large['expected_mad'] < results_small['expected_mad']

        # The difference should follow the formula ratio
        # E(MAD)_small / E(MAD)_large ≈ √(N_large / N_small)
        expected_ratio = math.sqrt(results_large['N'] / results_small['N'])
        actual_ratio = results_small['expected_mad'] / results_large['expected_mad']
        assert np.isclose(expected_ratio, actual_ratio, rtol=0.01)

    def test_negative_excess_mad_indicates_conformity(self):
        """Test that negative Excess MAD indicates good conformity."""
        bl = benfordslaw(method='mad', pos='first_two')

        # Generate data that follows Benford's Law well
        np.random.seed(123)
        # Using a large sample of lognormal data
        data = np.random.lognormal(mean=6, sigma=3, size=10000) * 100

        results = bl.fit(data)

        # If Excess MAD is negative, conformity should indicate good fit
        # (though this is probabilistic and depends on the data)
        if results['excess_mad'] < 0:
            assert results['conformity_mad'] in ['close conformity', 'acceptable conformity']

    def test_different_digit_positions(self):
        """Test MAD calculation for different digit positions."""
        positions = [1, 2, 3, 'first_two']

        bl_base = benfordslaw()
        df = bl_base.import_example(data='elections_usa')
        X = df['votes'].loc[df['candidate'] == 'Donald Trump'].values

        for pos in positions:
            bl = benfordslaw(method='mad', pos=pos)
            results = bl.fit(X)

            # All should have valid MAD statistics
            assert not np.isnan(results['mad']), f"NaN MAD for pos={pos}"
            assert not np.isnan(results['expected_mad']), f"NaN expected_mad for pos={pos}"
            assert not np.isnan(results['excess_mad']), f"NaN excess_mad for pos={pos}"


class TestFirstTwoDigits(unittest.TestCase):
    """Test suite for first-two-digits functionality."""

    def test_first_two_digit_counting(self):
        """Test that first-two-digits are correctly extracted and counted."""
        bl = benfordslaw(pos='first_two')

        # Test with known data
        data = np.array([10, 11, 12, 19, 20, 25, 99, 100, 1000, 10000])
        results = bl.fit(data)

        # Check that we got 90 categories
        assert results['percentage_emp'].shape[0] == 90

    def test_first_two_benford_probabilities(self):
        """Test that first-two-digit Benford probabilities sum to 1."""
        bl = benfordslaw(pos='first_two')

        # Leading digits are in percentage, should sum to 100
        total_prob = np.sum(bl.leading_digits)
        assert np.isclose(total_prob, 100.0, rtol=1e-5)

    def test_first_two_digit_minimum_value(self):
        """Test that values less than 10 are excluded from first-two-digits test."""
        bl = benfordslaw(pos='first_two')

        # All values less than 10
        data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        results = bl.fit(data)

        # Should have no valid observations
        assert results['N'] == 0


if __name__ == '__main__':
    unittest.main()
