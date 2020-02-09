import numpy as np
import benfordslaw as bl

def test_benfordslaw():
    df = bl.import_example('USA')
    Iloc = df['candidate']=='Donald Trump'
    X = df['votes'].loc[Iloc].values

    # TEST 1: check output is unchanged
    methods=[None, 'chi2', 'ks']
    for method in methods:
        out = bl.fit(X, method=method)
        assert [*out.keys()]==['P', 't', 'alpha', 'method', 'percentage_emp']

    # TEST 2: check chi2
    out = bl.fit(X, method='chi2')
    assert out['P']==0.44441032315455364
    assert out['t']==7.888769391226363
    # TEST 3: check ks
    out = bl.fit(X, method='ks')
    assert out['P']==1.0
    assert out['t']==0.1111111111111111
    # TEST 4: check percentages
    assert out['percentage_emp']==[31.64521544487969, 16.508114157806382, 12.479015109121432, 9.820928931169558, 7.862339115836598, 6.3794068270845, 5.8477895914941245, 4.616675993284835, 4.8405148293228875]
    