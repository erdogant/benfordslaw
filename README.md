# benfordslaw

[![Python](https://img.shields.io/pypi/pyversions/benfordslaw)](https://img.shields.io/pypi/pyversions/benfordslaw)
[![PyPI Version](https://img.shields.io/pypi/v/benfordslaw)](https://pypi.org/project/benfordslaw/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/erdogant/benfordslaw/blob/master/LICENSE)
[![BuyMeCoffee](https://img.shields.io/badge/buymeacoffee-grey.svg)](https://www.buymeacoffee.com/erdogant)
[![Github Forks](https://img.shields.io/github/forks/erdogant/benfordslaw.svg)](https://github.com/erdogant/benfordslaw/network)
[![GitHub Open Issues](https://img.shields.io/github/issues/erdogant/benfordslaw.svg)](https://github.com/erdogant/benfordslaw/issues)
[![Project Status](http://www.repostatus.org/badges/latest/active.svg)](http://www.repostatus.org/#active)
[![Downloads](https://pepy.tech/badge/benfordslaw/month)](https://pepy.tech/project/benfordslaw/month)
[![Downloads](https://pepy.tech/badge/benfordslaw)](https://pepy.tech/project/benfordslaw)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://erdogant.github.io/benfordslaw/pages/html/Documentation.html#colab-notebook)
[![Sphinx](https://img.shields.io/badge/Sphinx-Docs-Green)](https://erdogant.github.io/benfordslaw/)
[![DOI](https://zenodo.org/badge/239205250.svg)](https://zenodo.org/badge/latestdoi/239205250)
<!---[![Coffee](https://img.shields.io/badge/coffee-black-grey.svg)](https://erdogant.github.io/donate/?currency=USD&amount=5)-->

* ``benfordslaw`` is Python package to test if an empirical (observed) distribution differs significantly from a theoretical (expected, Benfords) distribution. The law states that in many naturally occurring collections of numbers, the leading significant digit is likely to be small. This method can be used if you want to test whether your set of numbers may be artificial (or manipulated). If a certain set of values follows Benford's Law then model's for the corresponding predicted values should also follow Benford's Law. Normal data (Unmanipulated) does trend with Benford's Law, whereas Manipulated or fraudulent data does not.

* Assumptions of the data:
  1. The numbers need to be random and not assigned, with no imposed minimums or maximums.
  2. The numbers should cover several orders of magnitude
  3. Dataset should preferably cover at least 1000 samples. Though Benford's law has been shown to hold true for datasets containing as few as 50 numbers.

# 
**⭐️ Star this repo if you like it ⭐️**
#

#### Install benfordslaw from PyPI

```bash
pip install benfordslaw
```

#### Import benfordslaw package

```python
from benfordslaw import benfordslaw
```
# 


### [Documentation pages](https://erdogant.github.io/benfordslaw/)

On the [documentation pages](https://erdogant.github.io/benfordslaw/) you can find detailed information about the working of the ``benfordslaw`` with many examples. 

<hr> 

### Examples

# 

* [Example: Analyze first digit-distribution](https://erdogant.github.io/benfordslaw/pages/html/Examples.html#second-digit-test)

<p align="left">
  <a href="https://erdogant.github.io/benfordslaw/pages/html/Examples.html#second-digit-test">
  <img src="https://github.com/erdogant/benfordslaw/blob/master/docs/figs/fig1.png" width="600" />
  </a>
</p>


# 

* [Example: Analyze second digit-distribution](https://erdogant.github.io/benfordslaw/pages/html/Examples.html)

<p align="left">
  <a href="https://erdogant.github.io/benfordslaw/pages/html/Examples.html">
  <img src="https://github.com/erdogant/benfordslaw/blob/master/docs/figs/fig2nd_digit_votes.png" width="600" />
  </a>
</p>


# 

* [Example: Analyze last digit-distribution](https://erdogant.github.io/benfordslaw/pages/html/Examples.html#last-digit-test)

<p align="left">
  <a href="https://erdogant.github.io/benfordslaw/pages/html/Examples.html#last-digit-test">
  <img src="https://github.com/erdogant/benfordslaw/blob/master/docs/figs/fig_last_digit_votes.png" width="600" />
  </a>
</p>


# 

* [Example: Analyze second last digit-distribution](https://erdogant.github.io/benfordslaw/pages/html/Examples.html#second-last-digit-test)

<p align="left">
  <a href="https://erdogant.github.io/benfordslaw/pages/html/Examples.html#second-last-digit-test">
  <img src="https://github.com/erdogant/benfordslaw/blob/master/docs/figs/fig_2nd_last_digit_votes.png" width="600" />
  </a>
</p>



#### References
* https://en.wikipedia.org/wiki/Benford%27s_law
* https://towardsdatascience.com/frawd-detection-using-benfords-law-python-code-9db8db474cf8

#### Citation
Please cite in your publications if this is useful for your research (see citation).
   
### Maintainers
* Erdogan Taskesen, github: [erdogant](https://github.com/erdogant)

### Contribute
* All kinds of contributions are welcome!
* If you wish to buy me a <a href="https://www.buymeacoffee.com/erdogant">Coffee</a> for this work, it is very appreciated :)

### Licence
See [LICENSE](LICENSE) for details.
