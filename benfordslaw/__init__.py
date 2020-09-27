from benfordslaw.benfordslaw import benfordslaw

__author__ = 'Erdogan Tasksen'
__email__ = 'erdogant@gmail.com'
__version__ = '1.0.1'

# module level doc-string
__doc__ = """
benfordslaw - benfordslaw is an Python package to test if an empirical (observed) distribution differs significantly from a theoretical (expected, Benfords) distribution.
=====================================================================

Description
-----------
Test if an empirical (observed) distribution differs significantly from a theoretical (expected, Benfords) distribution.
The law states that in many naturally occurring collections of numbers, the leading significant digit is likely to be small.
This method can be used if you want to test whether your set of numbers may be artificial (or manupilated).

Example
-------
>>> from benfordslaw import benfordslaw
>>> # Initialize
>>> bl = benfordslaw()
>>> df = bl.import_example()
>>> # Get data for one candidate
>>> X = df['votes'].loc[df['candidate']=='Donald Trump'].values
>>> # Fit
>>> results = bl.fit(X)
>>> # Figure
>>> fig, ax = bl.plot()

References
----------
https://github.com/erdogant/benfordslaw
See README.md file for more information.
"""
