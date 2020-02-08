# benfordslaw

[![Python](https://img.shields.io/pypi/pyversions/benfordslaw)](https://img.shields.io/pypi/pyversions/benfordslaw)
[![PyPI Version](https://img.shields.io/pypi/v/benfordslaw)](https://pypi.org/project/benfordslaw/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/erdogant/benfordslaw/blob/master/LICENSE)
[![Downloads](https://pepy.tech/badge/benfordslaw/week)](https://pepy.tech/project/benfordslaw/week)
[![Donate Bitcoin](https://img.shields.io/badge/donate-grey.svg)](https://erdogant.github.io/donate/?currency=USD&amount=5)

* benfordslaw is Python package

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
* It is advisable to create a new environment. 
```python
conda create -n env_benfordslaw python=3.6
conda activate env_benfordslaw
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
import benfordslaw as benfordslaw
```

#### Example:
```python
df = pd.read_csv('https://github.com/erdogant/hnet/blob/master/benfordslaw/data/example_data.csv')
model = benfordslaw.fit(df)
G = benfordslaw.plot(model)
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
* 
   
#### Maintainers
* Erdogan Taskesen, github: [erdogant](https://github.com/erdogant)

#### Contribute
* Contributions are welcome.

#### Licence
See [LICENSE](LICENSE) for details.

#### Donation
* This work is created and maintained in my free time. Contributions of any kind are very appreciated. <a href="https://erdogant.github.io/donate/?currency=USD&amount=5">Sponsering</a> is also possible.

