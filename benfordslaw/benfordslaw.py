"""benfordslaw is a python library to test the frequency distribution of leading digits."""

# --------------------------------------------------
# Name        : benfordslaw.py
# Author      : E.Taskesen
# Contact     : erdogant@gmail.com
# github      : github.com/erdogant/benfordslaw.py
# Licence     : MIT
# --------------------------------------------------


# Libraries
import os
import numpy as np
import pandas as pd
from scipy.stats import chisquare
from scipy.stats import ks_2samp
from scipy.stats import combine_pvalues
import matplotlib.pyplot as plt
import math
import datazets as dz


# %% Class
class benfordslaw:
    """Class benfordslaw."""

    def __init__(self, alpha=0.05, method='chi2', pos=1, verbose=3):
        """Initialize benfordslaw with user-defined parameters.

        Parameters
        ----------
        X : list or numpy array
            Input data.
        alpha : float [0-1], (default: 0.05).
            Only used to print message about statistical significant.
        method : string, (Default: 'chi2').
            * 'chi2'
            * 'ks'
            * None (combined pvalues based fishers-method)
        pos : int [-9,..,9], (default: 1).
            Digit position the be analyzed. 1: first digit, 2: second digit etc. -1: the last position, -2: second last digit etc
        verbose : int, optional
            Print message to screen. The default is 3.

        """
        if (alpha is None): alpha=1
        self.alpha = alpha
        self.method = method
        self.pos = pos
        self.verbose = verbose
        # Benford's Law percentage-distribution for leading digits 1-9
        if np.abs(pos)==1:
            self.leading_digits = np.array(list(map(lambda x: math.log(1 + (1 / x), 10), np.arange(1, 10)))) * 100
            self.digit_range = range(1, 10)
        elif np.abs(pos)==2:
            self.leading_digits = [12, 11.4, 10.9, 10.4, 10, 9.7, 9.3, 9, 8.8, 8.5]
            self.digit_range = range(0, 10)
        elif np.abs(pos)==3:
            self.leading_digits = [10.2, 10.1,	10.1, 10.1,	10.0, 10.0,	9.9, 9.9, 9.9, 9.8]
            self.digit_range = range(0, 10) 

        elif (np.abs(pos)>3) or (np.abs(pos)==0):
            raise Exception('[benfordslaw] >There is no leading digit distribution specified for this digit!')

    def fit(self, X):
        """Test if an empirical (observed) distribution significantly differs from a theoretical (expected, Benfords) distribution.

        The law states that in many naturally occurring collections of numbers, the leading significant digit is likely to be small.
        This method can be used if you want to test whether your set of numbers may be artificial (or manipulated).
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

        Examples
        --------
        >>> from benfordslaw import benfordslaw
        >>> # Initialize
        >>> bl = benfordslaw()
        >>> df = bl.import_example()
        >>> # Get data for one candidate
        >>> X = df['votes'].loc[df['candidate']=='Donald Trump'].values
        >>> # Fit
        >>> results = bl.fit(X)
        >>> # Figure
        >>> fig, ax = bl.plot()

        Returns
        -------
        dict.

        """
        # Make distribution first digits
        if self.verbose>=3: print("[benfordslaw] >Analyzing digit position: [%s]" %(self.pos))
        # Convert pandas dataframe to numpy array
        if isinstance(X, pd.DataFrame): X = X.values.ravel()
        # Count digit
        counts_emp, percentage_emp, total_count, digit = _count_digit(X, self.pos, self.digit_range)
        # Expected counts
        counts_exp = self._get_expected_counts(total_count)

        # Compute Pvalues
        if self.method=='chi2':
            try:
                tstats, Praw = chisquare(counts_emp, f_exp=counts_exp)
            except:
                raise Exception('The relative tolerance of the chisquare test is not reached. Try using another method such as "method=ks". This is not a bug but a feature: "https://github.com/scipy/scipy/issues/13362" ')
        elif self.method=='ks':
            tstats, Praw = ks_2samp(counts_emp, counts_exp)
        else:
            stats1, Praw1 = chisquare(counts_emp, f_exp=counts_exp)
            tstats2, Praw2 = ks_2samp(counts_emp, counts_exp)
            tstats, Praw = combine_pvalues([Praw1, Praw2], method='fisher')
            self.method = 'P_ensemble'

        # Show message
        if (Praw<=self.alpha) and (self.verbose>=3):
            print("[benfordslaw] >[%s] Anomaly detected! P=%g, Tstat=%g" %(self.method, Praw, tstats))
        elif self.verbose>=3:
            print("[benfordslaw] >[%s] No anomaly detected. P=%g, Tstat=%g" %(self.method, Praw, tstats))

        # Store
        self.results = {}
        self.results['P'] = Praw
        self.results['t'] = tstats
        self.results['P_significant'] = Praw<=self.alpha
        self.results['percentage_emp'] = np.c_[digit, percentage_emp]

        # return
        return self.results

    # Plot
    def plot(self, title='', fontsize=16, barcolor='black', barwidth=0.3, label='Empirical distribution', figsize=(15, 8)):
        """Make bar chart of observed vs expected 1st digit frequency in percent.

        Parameters
        ----------
        fontsize : int, (default : 16)
            Font size.
        barwidth : float, (default : 0.3)
            Width of the bars.
        barcolor : tuple or string, (default : 'black')
            Color of the bars. Can be of type String such as "red" or "black" but also RGB list such as: [0.5, 0.5, 0.5]
        label : String, (default : 'Empirical distribution')
            Label of the figure.
        figsize : tuple, optional
            Figure size. The default is (15,8).

        Returns
        -------
        tuple : fig, ax.

        """
        data_percentage = self.results['percentage_emp']
        x = data_percentage[:, 0]

        # Make figures
        fig, ax = plt.subplots(figsize=figsize)
        # Plot Empirical percentages
        rects1 = ax.bar(x, data_percentage[:, 1], width=barwidth, color=barcolor, alpha=0.8, label=label)
        plt.plot(x, data_percentage[:, 1], color='black', linewidth=0.8)
        # ax.scatter(x, data_percentage, s=150, c='red', zorder=2)
        # attach a text label above each bar displaying its height
        for rect in rects1:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2, height, '{:0.1f}'.format(height), ha='center', va='bottom', fontsize=13)

        # Plot expected benfords values
        ax.scatter(x, self.leading_digits, s=150, c='red', zorder=2, label='Benfords distribution')
        # ax.bar(x + width, BENFORDLD, width=width, color='blue', alpha=0.8, label='Benfords distribution')
        # plt.plot(x + width, BENFORDLD, color='blue', linewidth=0.8)

        if self.results['P']<=self.alpha:
            title = title + "\nAnomaly detected! P=%g, Tstat=%g" %(self.results['P'], self.results['t'])
        else:
            title = title + "\nNo anomaly detected. P=%g, Tstat=%g" %(self.results['P'], self.results['t'])

        # Add some text for labels, title and custom x-axis tick labels, etc.
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
        ax.legend(prop={'size': 15}, frameon=False)
        plt.show()
        return fig, ax

    def import_example(self, data='elections', url=None, sep=',', verbose=3):
        """Import example dataset from github source.

        Import one of the few datasets from github source or specify your own download url link.

        Parameters
        ----------
        data : str
            Example data sets:
            'elections_rus'
            'elections_usa'
        url : str
            url link to to dataset.
        sep : Seperator (String)
            When using URL, seperate the input file based on this seperator.

        Returns
        -------
        pd.DataFrame()
            Dataset containing mixed features.

        References
        ----------
            * https://github.com/erdogant/datazets

        """
        if data == 'elections_usa':
            url = 'https://erdogant.github.io/datasets/USA_2016_elections.zip'
            data = None
        elif data == 'elections_rus':
            url = 'https://erdogant.github.io/datasets/RUS_2018_elections.zip'
            data = None
        else:
            if verbose >= 3: print('[benfordslaw] >[%s] does not exists. Try "elections_usa" or "elections_rus" <return>' %(data))

        return dz.get(data=data, url=url, sep=sep)

    # Compute expected counts
    def _get_expected_counts(self, total_count):
        """Return list of expected Benford's Law counts for total sample count."""
        out = []
        for p in self.leading_digits:
            out.append((p * total_count / 100))
        return out


# %% Counts and the frequencies in percentage for the first digit
def _count_first_digit(data):
    # Get only non-zero values
    data = data[data>=1]

    # Get the first digits
    first_digits = list(map(lambda x: int(str(x)[0]), data))

    # Count occurences. Make sure every position is for [1-9]
    empirical_counts = np.zeros(9)
    digit = []
    for i in range(1, 10):
        empirical_counts[i - 1] = first_digits.count(i)
        digit.append(i)

    # Total amount
    total_count = sum(empirical_counts)
    # Make percentage
    empirical_percentage = [(i / total_count) * 100 for i in empirical_counts]
    # Return
    return(empirical_counts, empirical_percentage, total_count, digit)


# %% Counts and the frequencies in percentage for the second digit
def _count_digit(data, d, digit_range):
    # Get only non-zero values
    data = data[data>=1]

    # Reverse numbers if last digits is required
    if d < 0:
        data = list(map(lambda x: x[::-1], data.astype(str)))
        data = np.array(data).astype(int)
        d = d * -1

    # Remove one because pythons starts counting from 0
    d = d - 1

    # Get the ith digit
    digits = np.zeros_like(data)
    Iloc = data>=np.power(10, d)
    Iloc[np.isnan(Iloc)]=False
    Iloc = Iloc.astype(bool)
    digits[Iloc] = list(map(lambda x: int(str(x)[d]), data[Iloc]))

    # Count occurences. Make sure every position is for [1-9]
    empirical_counts = np.zeros(len(digit_range))
    digitnr = []
    for i in digit_range:
        empirical_counts[i - digit_range[0]] = list(digits[Iloc]).count(i)
        digitnr.append(i)

    # Total amount
    total_count = sum(empirical_counts)
    # Make percentage
    empirical_percentage = [(i / total_count) * 100 for i in empirical_counts]
    # Return
    return(empirical_counts, empirical_percentage, total_count, digitnr)


# %% Main
if __name__ == "__main__":
    print('[benfordslaw] >Please bootup python and run benfordslaw as described in the readme file: https://github.com/erdogant/benfordslaw')
