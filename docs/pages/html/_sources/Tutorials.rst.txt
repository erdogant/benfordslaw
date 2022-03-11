Input
###########################

The input for ``benfordslaw`` is a vector with numerical values that can either be a ``list`` or ``np.array``. 


.. code:: python

	# Import library
	import numpy as np
	from benfordslaw import benfordslaw

	# Create uniform random data which does definitely not follow Benfords distribution.
	X = np.random.randint(0, high=100, size=1000)

	# Initialize with alpha and method.
	bl = benfordslaw(alpha=0.05, method='chi2')

	print(X)
	# array([13, 12,  2,  4, 99, 33, 71, 69, 65, 55,  6, 30, 30, 99, 43, 36, 12,....]

	# Fit
	results = bl.fit(X)

	# As expected, a significant P-value is detected for the inupt data X
	# [benfordslaw] >Analyzing digit position: [1]
	# [benfordslaw] >[chi2] Anomaly detected! P=3.46161e-73, Tstat=361.323

	# Plot
	bl.plot(title='Random data')


Output
###########################

The output of ``benfordslaw`` :func:`benfordslaw.benfordslaw.fit` is a dictionary with the following keys:

	* P		 : P-value
	* t		 : t-statistic
	* P_significant	 : Boolean value that is set by alpha
	* percentage_emp : Percentage distribution digits


.. raw:: html

	<hr>
	<center>
		<script async type="text/javascript" src="//cdn.carbonads.com/carbon.js?serve=CEADP27U&placement=erdogantgithubio" id="_carbonads_js"></script>
	</center>
	<hr>
