# pip install pytest
# pytest test/test_benfordslaw.py

import numpy as np
from benfordslaw import benfordslaw
import unittest

class TestCLUSTIMAGE(unittest.TestCase):

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
