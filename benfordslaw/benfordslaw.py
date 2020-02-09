"""Test if an empirical (observed) distribution differs significantly from a theoretical (expected, Benfords) distribution."""

# --------------------------------------------------
# Name        : benfordslaw.py
# Author      : E.Taskesen
# Contact     : erdogant@gmail.com
# github      : https://github.com/erdogant/benfordslaw.py
# Licence     : MIT
# --------------------------------------------------


# %% Libraries
import os
import numpy as np
import pandas as pd
from scipy.stats import chisquare
from scipy.stats import ks_2samp
from scipy.stats import combine_pvalues
import matplotlib.pyplot as plt
# Benford's Law percentage-distribution for leading digits 1-9
BENFORDLD = [30.1, 17.6, 12.5, 9.7, 7.9, 6.7, 5.8, 5.1, 4.6]


# %% Fit
def fit(X, alpha=0.05, method=None, verbose=3):
    """Test if an empirical (observed) distribution significantly differs from a theoretical (expected, Benfords) distribution.

    Description
    -----------
    The law states that in many naturally occurring collections of numbers, the leading significant digit is likely to be small.
    This method can be used if you want to test whether your set of numbers may be artificial (or manupilated).
    Let us assume the null Hypothesis: H0: observed and theoretical distributions are the same.
    If a certain set of values follows Benford's Law then model's for the corresponding predicted values should also follow Benford's Law.
    Normal data (Unmanipulated) does trend with Benford's Law, whereas Manipulated or fraudulent data does not.

   Assumptions of the data:
       1. The numbers need to be random and not assigned, with no imposed minimums or maximums.
       2. The numbers should cover several orders of magnitude
       3. Dataset should preferably cover at least 1000 samples. Though Benford’s law has been shown to hold true for datasets containing as few as 50 numbers.


    Parameters
    ----------
    X : list or numpy array
        Input data.
    alpha : float [0-1], optional
        Only used to print message about statistical significant. The default is 0.05.
    method : string, optional
        None (Default: combined pvalues based fishers-method)
        'chi2'
        'ks'
    verbose : int, optional
        Print message to screen. The default is 3.

    Returns
    -------
    dict.

    """
    # Make distribution first digits
    [counts_emp, percentage_emp, total_count] = _count_first_digit(X)
    # Expected counts
    counts_exp = _get_expected_counts(total_count)

    # Compute Pvalues
    if method=='chi2':
        [tstats, Praw] = chisquare(counts_emp, f_exp=counts_exp)
    elif method=='ks':
        [tstats, Praw] = ks_2samp(counts_emp, counts_exp)
    else:
        [tstats1, Praw1] = chisquare(counts_emp, f_exp=counts_exp)
        [tstats2, Praw2] = ks_2samp(counts_emp, counts_exp)
        tstats, Praw = combine_pvalues([Praw1, Praw2], method='fisher')
        method='P_ensemble'

    if Praw<=alpha and verbose>=3:
        print("[BL.fit][%s] Anomaly detected! P=%g, Tstat=%g" %(method, Praw, tstats))
    elif verbose>=3:
        print("[BL.fit][%s] No anomaly detected. P=%g, Tstat=%g" %(method, Praw, tstats))

    out = {}
    out['P'] = Praw
    out['t'] = tstats
    out['alpha'] = alpha
    out['method'] = method
    # out['counts_exp'] = counts_exp
    # out['counts_emp'] = counts_emp
    out['percentage_emp'] = percentage_emp

    # return
    return(out)


# %% Final counts and the frequencies in percentage.
def _count_first_digit(data):
    # Get only non-zero values
    data=data[data>1]
    # Get the first digits
    first_digits=list(map(lambda x: int(str(x)[0]), data))

    # Count occurences. Make sure every position is for [1-9]
    emperical_counts = np.zeros(9)
    for i in range(1,10):
        emperical_counts[i - 1] = first_digits.count(i)

    # Total amount
    total_count=sum(emperical_counts)
    # Make percentage
    emperical_percentage=[(i / total_count) * 100 for i in emperical_counts]
    # Return
    return(emperical_counts, emperical_percentage, total_count)


# %% Compute expected counts
def _get_expected_counts(total_count):
    """Return list of expected Benford's Law counts for total sample count."""
    out=[]
    for p in BENFORDLD:
        out.append(round(p * total_count / 100))

    return(out)


# %% Plot
def plot(out, title='', figsize=(15,8)):
    """Make bar chart of observed vs expected 1st digit frequency in percent.

    Parameters
    ----------
    out : dict
        output of the fit() function.
    figsize : tuple, optional
        Figure size. The default is (15,8).

    Returns
    -------
    fig,ax.

    """
    fontsize=16

    data_percentage = out['percentage_emp']
    x = np.arange(len(data_percentage))
    width = 0.3  # the width of the bars

    fig, ax = plt.subplots(figsize=figsize)
    # Plot emperical percentages
    rects1 = ax.bar(x, data_percentage, width=width, color='black', alpha=0.8, label='Emperical distribution')
    plt.plot(x, data_percentage, color='black', linewidth=0.8)
    ax.scatter(x, data_percentage, s=150, c='red', zorder=2)
    # attach a text label above each bar displaying its height
    for rect in rects1:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2, height, '{:0.1f}'.format(height), ha='center', va='bottom', fontsize=13)

    # Plot expected benfords values
    ax.bar(x + width, BENFORDLD, width=width, color='blue', alpha=0.8, label='Benfords distribution')
    plt.plot(x + width, BENFORDLD, color='blue', linewidth=0.8)

    if out['P']<=out['alpha']:
        title = title + "\nAnomaly detected! P=%g, Tstat=%g" %(out['P'], out['t'])
    else:
        title = title + "\nNo anomaly detected. P=%g, Tstat=%g" %(out['P'], out['t'])

    # Add some text for labels, title and custom x-axis tick labels, etc.
    fig.canvas.set_window_title('Percentage First Digits')
    ax.set_title(title, fontsize=fontsize)
    ax.set_ylabel('Frequency (%)', fontsize=fontsize)
    ax.set_xlabel('Digits', fontsize=fontsize)
    ax.set_xticks(x)
    ax.set_xticklabels(x, fontsize=fontsize)
    ax.grid(True)
    ax.legend()
    # Hide the right and top spines & add legend
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.legend(prop={'size':15}, frameon=False)
    plt.show()

    return fig,ax


# %% Example data
def import_example(getfile='USA'):
    """Import example.

    Parameters
    ----------
    getfile : String, optional
        'USA_2016_election_primary_results.zip'

    Returns
    -------
    df : DataFrame

    """
    if getfile=='USA':
        getfile='USA_2016_election_primary_results.zip'
    else:
        getfile='RUS_2018_voting_data_eng.zip'

    print('[BL.import_example] Loading %s..' %getfile)
    curpath = os.path.dirname(os.path.abspath(__file__))
    PATH_TO_DATA=os.path.join(curpath, 'data', getfile)
    if os.path.isfile(PATH_TO_DATA):
        df=pd.read_csv(PATH_TO_DATA, sep=',')
        return df
    else:
        print('[BL.import_example] Oops! Example data not found!')
        return None
