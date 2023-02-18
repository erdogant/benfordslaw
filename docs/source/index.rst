benfordslaw
===========

.. |figd| image:: ../figs/fig1.png

.. table:: 
   :align: center

   +----------+
   | |figd|   |
   +----------+

-----------------------------------

|python| |pypi| |docs| |LOC| |downloads_month| |downloads_total| |license| |forks| |open issues| |project status| |colab| |DOI| |donate|

.. include:: add_top.add

``benfordslaw`` is Python package to test if an empirical (observed) distribution differs significantly from a theoretical (expected, Benfords) distribution. The law states that in many naturally occurring collections of numbers, the leading significant digit is likely to be small. This method can be used if you want to test whether your set of numbers may be artificial (or manipulated). If a certain set of values follows Benford's Law then model's for the corresponding predicted values should also follow Benford's Law. Normal data (unmanipulated) does trend with Benford's Law, whereas manipulated or fraudulent data does not.

**Assumptions of the data**

	* The numbers need to be random and not assigned, with no imposed minimums or maximums.
	* The numbers should cover several orders of magnitude
	* Dataset should preferably cover at least 1000 samples. Though Benford's law has been shown to hold true for datasets containing as few as 50 numbers.



Contents
========

.. toctree::
   :maxdepth: 1
   :caption: Installation
   
   Installation


.. toctree::
  :maxdepth: 1
  :caption: Tutorials

  Tutorials


.. toctree::
  :maxdepth: 1
  :caption: Examples

  Examples

.. toctree::
  :maxdepth: 1
  :caption: Documentation
  
  Documentation
  Coding quality
  




Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`




.. |python| image:: https://img.shields.io/pypi/pyversions/benfordslaw.svg
    :alt: |Python
    :target: https://erdogant.github.io/benfordslaw/

.. |pypi| image:: https://img.shields.io/pypi/v/benfordslaw.svg
    :alt: |Python Version
    :target: https://pypi.org/project/benfordslaw/

.. |docs| image:: https://img.shields.io/badge/Sphinx-Docs-blue.svg
    :alt: Sphinx documentation
    :target: https://erdogant.github.io/benfordslaw/

.. |LOC| image:: https://sloc.xyz/github/erdogant/benfordslaw/?category=code
    :alt: lines of code
    :target: https://github.com/erdogant/benfordslaw

.. |downloads_month| image:: https://static.pepy.tech/personalized-badge/benfordslaw?period=month&units=international_system&left_color=grey&right_color=brightgreen&left_text=PyPI%20downloads/month
    :alt: Downloads per month
    :target: https://pepy.tech/project/benfordslaw

.. |downloads_total| image:: https://static.pepy.tech/personalized-badge/benfordslaw?period=total&units=international_system&left_color=grey&right_color=brightgreen&left_text=Downloads
    :alt: Downloads in total
    :target: https://pepy.tech/project/benfordslaw

.. |license| image:: https://img.shields.io/badge/license-MIT-green.svg
    :alt: License
    :target: https://github.com/erdogant/benfordslaw/blob/master/LICENSE

.. |forks| image:: https://img.shields.io/github/forks/erdogant/benfordslaw.svg
    :alt: Github Forks
    :target: https://github.com/erdogant/benfordslaw/network

.. |open issues| image:: https://img.shields.io/github/issues/erdogant/benfordslaw.svg
    :alt: Open Issues
    :target: https://github.com/erdogant/benfordslaw/issues

.. |project status| image:: http://www.repostatus.org/badges/latest/active.svg
    :alt: Project Status
    :target: http://www.repostatus.org/#active

.. |donate| image:: https://img.shields.io/badge/Support%20this%20project-grey.svg?logo=github%20sponsors
    :alt: donate
    :target: https://erdogant.github.io/benfordslaw/pages/html/Documentation.html#

.. |colab| image:: https://colab.research.google.com/assets/colab-badge.svg
    :alt: Colab example
    :target: https://erdogant.github.io/benfordslaw/pages/html/Documentation.html#colab-notebook

.. |DOI| image:: https://zenodo.org/badge/239205250.svg
    :alt: Cite
    :target: https://zenodo.org/badge/latestdoi/239205250


.. include:: add_bottom.add