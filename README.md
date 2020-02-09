# benfordslaw

[![Python](https://img.shields.io/pypi/pyversions/benfordslaw)](https://img.shields.io/pypi/pyversions/benfordslaw)
[![PyPI Version](https://img.shields.io/pypi/v/benfordslaw)](https://pypi.org/project/benfordslaw/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/erdogant/benfordslaw/blob/master/LICENSE)
[![Downloads](https://pepy.tech/badge/benfordslaw/week)](https://pepy.tech/project/benfordslaw/week)
[![Donate Bitcoin](https://img.shields.io/badge/donate-grey.svg)](https://erdogant.github.io/donate/?currency=USD&amount=5)

* benfordslaw is Python package to test if an empirical (observed) distribution differs significantly from a theoretical (expected, Benfords) distribution. The law states that in many naturally occurring collections of numbers, the leading significant digit is likely to be small. This method can be used if you want to test whether your set of numbers may be artificial (or manupilated). If a certain set of values follows Benford's Law then model's for the corresponding predicted values should also follow Benford's Law. Normal data (Unmanipulated) does trend with Benford's Law, whereas Manipulated or fraudulent data does not.

* Assumptions of the data:
  1. The numbers need to be random and not assigned, with no imposed minimums or maximums.
  2. The numbers should cover several orders of magnitude
  3. Dataset should preferably cover at least 1000 samples. Though Benford’s law has been shown to hold true for datasets containing as few as 50 numbers.

### Contents
- [Installation](#-installation)
- [Requirements](#-Requirements)
- [Quick Start](#-quick-start)
- [Contribute](#-contribute)
- [Citation](#-citation)
- [Maintainers](#-maintainers)
- [License](#-copyright)

### Installation
* Install benfordslaw from PyPI (recommended). benfordslaw is compatible with Python 3.6+ and runs on Linux, MacOS X and Windows. 
* It is distributed under the MIT license.

### Requirements
```python
pip install -r requirements
```

#### Quick Start
```
pip install benfordslaw
```

* Alternatively, install benfordslaw from the GitHub source:
```bash
git clone https://github.com/erdogant/benfordslaw.git
cd benfordslaw
python setup.py install
```  

#### Import benfordslaw package
```python
import benfordslaw as bl

# Load elections example
df = bl.import_example()
# Extract election information.
Iloc = df['candidate']=='Donald Trump'
X = df['votes'].loc[Iloc].values
# Print
print(X)
# array([ 5387, 23618,  1710, ...,    16,    21,     0], dtype=int64)
# Make fit
out = bl.fit(X)
# Plot
bl.plot(out, title='Donald Trump')
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
   
#### Maintainers
* Erdogan Taskesen, github: [erdogant](https://github.com/erdogant)

#### Contribute
* Contributions are welcome.

#### Licence
See [LICENSE](LICENSE) for details.

#### Donation
* This work is created and maintained in my free time. Contributions of any kind are very appreciated. <a href="https://erdogant.github.io/donate/?currency=USD&amount=5">Sponsering</a> is also possible.

