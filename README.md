# benfordslaw

[![Python](https://img.shields.io/pypi/pyversions/benfordslaw)](https://img.shields.io/pypi/pyversions/benfordslaw)
[![PyPI Version](https://img.shields.io/pypi/v/benfordslaw)](https://pypi.org/project/benfordslaw/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/erdogant/benfordslaw/blob/master/LICENSE)
[![Coffee](https://img.shields.io/badge/coffee-black-grey.svg)](https://erdogant.github.io/donate/?currency=USD&amount=5)
[![Github Forks](https://img.shields.io/github/forks/erdogant/benfordslaw.svg)](https://github.com/erdogant/benfordslaw/network)
[![GitHub Open Issues](https://img.shields.io/github/issues/erdogant/benfordslaw.svg)](https://github.com/erdogant/benfordslaw/issues)
[![Project Status](http://www.repostatus.org/badges/latest/active.svg)](http://www.repostatus.org/#active)
[![Downloads](https://pepy.tech/badge/benfordslaw/month)](https://pepy.tech/project/benfordslaw/month)
[![Downloads](https://pepy.tech/badge/benfordslaw)](https://pepy.tech/project/benfordslaw)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/erdogant/benfordslaw/blob/master/notebooks/benfordslaw.ipynb)

* ``benfordslaw`` is Python package to test if an empirical (observed) distribution differs significantly from a theoretical (expected, Benfords) distribution. The law states that in many naturally occurring collections of numbers, the leading significant digit is likely to be small. This method can be used if you want to test whether your set of numbers may be artificial (or manupilated). If a certain set of values follows Benford's Law then model's for the corresponding predicted values should also follow Benford's Law. Normal data (Unmanipulated) does trend with Benford's Law, whereas Manipulated or fraudulent data does not.

* Assumptions of the data:
  1. The numbers need to be random and not assigned, with no imposed minimums or maximums.
  2. The numbers should cover several orders of magnitude
  3. Dataset should preferably cover at least 1000 samples. Though Benford's law has been shown to hold true for datasets containing as few as 50 numbers.


### Installation
* Install ``benfordslaw`` from PyPI (recommended). benfordslaw is compatible with Python 3.6+ and runs on Linux, MacOS X and Windows. 
* It is distributed under the MIT license.

#### Installation
```
pip install benfordslaw
```

* Alternatively, install benfordslaw from the GitHub source:
```bash
git clone https://github.com/erdogant/benfordslaw.git
cd benfordslaw
pip install -U .
```  

#### Import benfordslaw package
```python
from benfordslaw import benfordslaw

# Initialize
bl = benfordslaw()

# Load elections example
df = bl.import_example(data='USA')

# Extract election information.
X = df['votes'].loc[df['candidate']=='Donald Trump'].values

# Print
print(X)
# array([ 5387, 23618,  1710, ...,    16,    21,     0], dtype=int64)

# Make fit
results = bl.fit(X)

# Plot
bl.plot(title='Donald Trump')
```
<p align="center">
  <img src="https://github.com/erdogant/benfordslaw/blob/master/docs/figs/fig1.png" width="600" />
</p>

#### Citation
Please cite benfordslaw in your publications if this is useful for your research. Here is an example BibTeX entry:
```BibTeX
@misc{erdogant2020benfordslaw,
  title={benfordslaw},
  author={Erdogan Taskesen},
  year={2019},
  howpublished={\url{https://github.com/erdogant/benfordslaw}},
}
```

#### References
* https://en.wikipedia.org/wiki/Benford%27s_law
* https://towardsdatascience.com/frawd-detection-using-benfords-law-python-code-9db8db474cf8
   
### Maintainer
* Erdogan Taskesen, github: [erdogant](https://github.com/erdogant)
* This work is created and maintained in my free time. If you wish to buy me a <a href="https://erdogant.github.io/donate/?currency=USD&amount=5">Coffee</a> for this work, it is very appreciated.
* Contributions are welcome.
* Star it if you like it!
