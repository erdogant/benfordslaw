# pip install pytest
# pytest test/test_benfordslaw.py

import numpy as np
from benfordslaw import benfordslaw
import unittest

class TestBENFORDSLAW(unittest.TestCase):
    def test_benfordslaw_digits(self):
        gt = {-6: True, -5: True, -4: True, -3: True, -2: True, -1: True, 1: True, 2: True, 3: True, 4: True, 5: True, 6: True}
        total_results = []
        pos = [-9, -8, -7, -6, -5, -4, -3, -2 -1, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        for p, t in zip(pos, gt):
            bl = benfordslaw(pos=p, verbose=0)
            df = bl.import_example(data='elections_usa', verbose=0)
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
            assert np.all(np.isin([*out.keys()], ['P', 't', 'percentage_emp', 'P_significant']))

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
        np.all(np.isin([*results.keys()], ['P', 't', 'percentage_emp', 'P_significant']))
        assert np.all(results['percentage_emp'][:,1]==[31.64521544487969, 16.508114157806382, 12.479015109121432, 9.820928931169558, 7.862339115836598, 6.3794068270845, 5.8477895914941245, 4.616675993284835, 4.8405148293228875])
