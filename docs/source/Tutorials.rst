Input
###########################

The input for ``benfordslaw`` can be either a list of integers or strings. 

.. code:: python

	# Import library
	import benfordslaw as benfordslaw
	
	# Target labels
	y=[1, 1, 2, 2, 3]

	# String as input labels
	y=["1", "1", "2", "2", "3"]
	
	# Generate colors
	c_rgb, c_dict = benfordslaw.fromlist(y)


Each of these input arrays can be in the form of:

	* List
	* Numpy Array


Output
###########################

The output of ``benfordslaw`` is a numpy array with RGB colors that range between [0-1, 0-1, 0-1].
In case of using the ``fromlist`` :func:`benfordslaw.benfordslaw.fromlist`, a dictionary is also returned with the keys as input label and colors as items.



.. raw:: html

	<hr>
	<center>
		<script async type="text/javascript" src="//cdn.carbonads.com/carbon.js?serve=CEADP27U&placement=erdogantgithubio" id="_carbonads_js"></script>
	</center>
	<hr>
