First digit test
####################################

In the following example we load the 2016 elections data of the USA for various candidates.
We will check whether the votes are fraudulent based on benfords distribution.

.. code:: python

	from benfordslaw import benfordslaw

	# Initialize
	bl = benfordslaw(pos=1, alpha=0.05)

	# Load elections example
	df = bl.import_example(data='elections_usa')

	# Extract election information.
	X = df['votes'].loc[df['candidate']=='Donald Trump'].values

	# Print
	print(X)
	# array([ 5387, 23618,  1710, ...,    16,    21,     0], dtype=int64)

	# Make fit
	results = bl.fit(X)

	# Plot
	bl.plot(title='Donald Trump')


.. |fig1| image:: ../figs/fig1.png

.. table:: First digit.
   :align: center

   +----------+
   | |fig1|   |
   +----------+



Second digit test
####################################

Let's check the the votes on the second digit and determine whether it significantly deviates from benfords distribution.

.. code:: python

	from benfordslaw import benfordslaw

	# Initialize
	bl = benfordslaw(pos=2)

	# Load elections example
	df = bl.import_example(data='elections_usa')

	# Extract election information.
	X = df['votes'].loc[df['candidate']=='Donald Trump'].values

	# Make fit
	results = bl.fit(X)

	# Plot
	bl.plot(title='Results of Donald Trump based on digit=2', barcolor=[0.5, 0.5, 0.5], fontsize=12, barwidth=0.4)


.. |fig2| image:: ../figs/fig2nd_digit_votes.png

.. table:: Second digit.
   :align: center

   +----------+
   | |fig2|   |
   +----------+



Third digit test
####################################

Let's check the the votes on the second digit and determine whether it significantly deviates from benfords distribution.

.. code:: python

	from benfordslaw import benfordslaw

	# Initialize
	bl = benfordslaw(pos=3)

	# Load elections example
	df = bl.import_example(data='elections_usa')

	# Extract election information.
	X = df['votes'].loc[df['candidate']=='Donald Trump'].values

	# Make fit
	results = bl.fit(X)

	# Plot
	bl.plot(title='Results of Donald Trump based on digit=3', barcolor=[0.5, 0.5, 0.5], fontsize=12, barwidth=0.4)


.. |fig6| image:: ../figs/fig6.png

.. table:: Second digit.
   :align: center

   +----------+
   | |fig6|   |
   +----------+




Last digit test
####################################

Let's check the the votes on the **last digit** and determine whether it significantly deviates from benfords distribution.

.. code:: python

	from benfordslaw import benfordslaw

	# Initialize
	bl = benfordslaw(pos=-1)

	# Load elections example
	df = bl.import_example(data='elections_usa')

	# Extract election information.
	X = df['votes'].loc[df['candidate']=='Donald Trump'].values

	# Make fit
	results = bl.fit(X)

	# Plot
	bl.plot(title='Results of Donald Trump based on digit=-1', barcolor=[0.5, 0.5, 0.5], fontsize=12, barwidth=0.4)


.. |fig3| image:: ../figs/fig_last_digit_votes.png

.. table:: Last digit.
   :align: center

   +----------+
   | |fig3|   |
   +----------+


Second last digit test
####################################

Let's check the the votes on the **last digit** and determine whether it significantly deviates from benfords distribution.

.. code:: python

	from benfordslaw import benfordslaw

	# Initialize
	bl = benfordslaw(pos=-2)

	# Load elections example
	df = bl.import_example(data='elections_usa')

	# Extract election information.
	X = df['votes'].loc[df['candidate']=='Donald Trump'].values

	# Make fit
	results = bl.fit(X)

	# Plot
	bl.plot(title='Results of Donald Trump based on digit=-2', barcolor=[0.5, 0.5, 0.5], fontsize=12, barwidth=0.4)


.. |fig4| image:: ../figs/fig_2nd_last_digit_votes.png

.. table:: Second last digit.
   :align: center

   +----------+
   | |fig4|   |
   +----------+



All other digits [4-9]
####################################

Benford's Law has known distributions for the the first three digits. All digits that come after (like pos=4), the distribution is not explicitly defined in classical Benford's Law. The significance of Benford's Law in data declines as you move to higher digit positions, since the influence of digit distributions decreases and approaches uniformity.
Therefore, I assume a uniform distribution for every position > 3 or position < 3.


.. code:: python

	from benfordslaw import benfordslaw

	# Initialize
	bl = benfordslaw(pos=4)

	# Load elections example
	df = bl.import_example(data='elections_usa')

	# Extract election information.
	X = df['votes'].loc[df['candidate']=='Donald Trump'].values

	# Make fit
	results = bl.fit(X)

	# Plot
	bl.plot(title='Results of Donald Trump based on digit=4', barcolor=[0.5, 0.5, 0.5], fontsize=12, barwidth=0.4)


.. |fig5| image:: ../figs/fig5.png

.. table:: Fourth digit.
   :align: center

   +----------+
   | |fig5|   |
   +----------+


.. include:: add_bottom.add