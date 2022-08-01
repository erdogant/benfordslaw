benfordslaw's documentation!
============================

``benfordslaw`` is Python package to test if an empirical (observed) distribution differs significantly from a theoretical (expected, Benfords) distribution. The law states that in many naturally occurring collections of numbers, the leading significant digit is likely to be small. This method can be used if you want to test whether your set of numbers may be artificial (or manipulated). If a certain set of values follows Benford's Law then model's for the corresponding predicted values should also follow Benford's Law. Normal data (unmanipulated) does trend with Benford's Law, whereas manipulated or fraudulent data does not.


Assumptions of the data
-----------------------
	* The numbers need to be random and not assigned, with no imposed minimums or maximums.
	* The numbers should cover several orders of magnitude
	* Dataset should preferably cover at least 1000 samples. Though Benford's law has been shown to hold true for datasets containing as few as 50 numbers.

.. |figd| image:: ../figs/fig1.png

.. table:: First digit.
   :align: center

   +----------+
   | |figd|   |
   +----------+


Sponsor
=======
**This library is created and maintained in my free time**, and I like to work on my open-source libraries!
If you like this library too, you can help by becoming a sponsor! The easiest way is by simply following me on medium, and it will cost you nothing! In return, you will receive the blogs that I write! Simply go to my `medium profile <https://erdogant.medium.com/>`_ and press "follow".
Read more on my `sponsor github page <https://github.com/sponsors/erdogant/>`_ why this is important. This also gives you various other ways to sponsor me!



Star is important too!
======================
If you like this project, **star** this repo at the github page! This is important because only then I know how much you like it :)


Content
=======

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
  benfordslaw.benfordslaw

* :ref:`genindex`


Quick install
-------------

.. code-block:: console

   pip install benfordslaw




Github
------------------------------

Please report bugs, issues and feature extensions there.
Github, `erdogant/benfordslaw <https://github.com/erdogant/benfordslaw/>`_.


Citing *benfordslaw*
-----------------------

The bibtex can be found in the right side menu at the `github page <https://github.com/erdogant/benfordslaw/>`_.



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. raw:: html

	<hr>
	<center>
		<script async type="text/javascript" src="//cdn.carbonads.com/carbon.js?serve=CEADP27U&placement=erdogantgithubio" id="_carbonads_js"></script>
	</center>
	<hr>

