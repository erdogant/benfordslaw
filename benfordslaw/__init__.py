from benfordslaw.benfordslaw import benfordslaw
from benfordslaw.benfordslaw import compute_excess_mad
from benfordslaw.benfordslaw import EXCESS_MAD_CONSTANTS

__author__ = 'Erdogan Tasksen'
__email__ = 'erdogant@gmail.com'
__version__ = '2.0.2'

# module level doc-string
__doc__ = """
benfordslaw is a python library to test the frequency distribution of leading digits.
=====================================================================================

Test if an empirical (observed) distribution differs significantly from a theoretical (expected, Benfords) distribution.
The law states that in many naturally occurring collections of numbers, the leading significant digit is likely to be small.
This method can be used if you want to test whether your set of numbers may be artificial (or manipulated).

New in version 2.0.2:
- Added Excess MAD (Mean Absolute Deviation) statistic for more reliable fraud detection
- Added first-two-digits test (pos='first_two') for higher resolution analysis
- Added 'mad' method option for MAD-based conformity assessment

Example
-------
>>> # Import library
>>> from benfordslaw import benfordslaw
>>> #
>>> # Initialize with MAD method (recommended for fraud detection)
>>> bl = benfordslaw(pos='first_two', method='mad')
>>> #
>>> df = bl.import_example()
>>> # Get data for one candidate
>>> X = df['votes'].loc[df['candidate']=='Donald Trump'].values
>>> #
>>> # Fit
>>> results = bl.fit(X)
>>> #
>>> # Access Excess MAD results
>>> print(f"Excess MAD: {results['excess_mad']}")
>>> print(f"Conformity: {results['conformity']}")
>>> #
>>> # Figure
>>> fig, ax = bl.plot()

Quick Excess MAD Computation
----------------------------
>>> from benfordslaw import compute_excess_mad
>>> result = compute_excess_mad(data, pos='first_two')
>>> print(f"Excess MAD: {result['excess_mad']}")

References
----------
* Barney, B. J., & Schulzke, K. S. (2016). Moderating "Cry Wolf" Events with Excess MAD
  in Benford's Law Research and Practice. Journal of Forensic Accounting Research, 1(1), A66-A90.
* https://github.com/erdogant/benfordslaw
See README.md file for more information.
"""
