"""benfordslaw is a python library to test the frequency distribution of leading digits.

 Name        : benfordslaw.py
 Author      : E.Taskesen
 Contact     : erdogant@gmail.com
 github      : github.com/erdogant/benfordslaw.py
 Licence     : MIT

"""
import datazets as dz
import numpy as np
import pandas as pd
from scipy.stats import chisquare
from scipy.stats import ks_2samp
from scipy.stats import combine_pvalues
import matplotlib.pyplot as plt
import math
import logging

logger = logging.getLogger(__name__)

# %% Class
class benfordslaw:
    """Class benfordslaw."""

    def __init__(self, alpha: float = 0.05, method: str = 'chi2', pos: int = 1, verbose: [str, int] = 'info',):
        """Initialize benfordslaw with user-defined parameters.

        Constants for Excess MAD calculation.
        The constants are derived from the variance of the binomial distribution for each digit test.
        For the first-two-digits test, C = 158.8 as derived in Barney & Schulzke (2016).
        For other tests, constants are computed using the formula: C = K^2 * π / (2 * (Σ sqrt(p_k * (1 - p_k)))^2), where K is the number of digit categories and p_k are the Benford probabilities.

        Parameters
        ----------
        X : list or numpy array
            Input data.
        alpha : float [0-1], (default: 0.05).
            Only used to print message about statistical significant.
        method : string, (Default: 'chi2').
            * 'chi2' : Chi-square test
            * 'ks' : Kolmogorov-Smirnov test
            * 'mad' : Mean Absolute Deviation with Excess MAD adjustment (recommended for fraud detection)
            * None : Combined p-values based on Fisher's method
        pos : int or str [-9,..,9] or 'first_two', (default: 1).
            Digit position to be analyzed.
            * 1: first digit
            * 2: second digit
            * 3: third digit (etc.)
            * -1: last digit
            * -2: second last digit (etc.)
            * 'first_two': First two digits combined (recommended for Benford's Law analysis,
              provides higher resolution with 90 categories instead of 9)
        verbose : str or int, optional, default='info' (20)
            Logging verbosity level. Possible values:
            - 0, 60, None, 'silent', 'off', 'no' : no messages.
            - 10, 'debug' : debug level and above.
            - 20, 'info' : info level and above.
            - 30, 'warning' : warning level and above.
            - 50, 'critical' : critical level and above.

        References
        ----------
        * Barney, B. J., & Schulzke, K. S. (2016). Moderating "Cry Wolf" Events with Excess MAD
          in Benford's Law Research and Practice. Journal of Forensic Accounting Research, 1(1), A66-A90.

        """
        # Set the logger
        verbose = set_logger(verbose=verbose)

        if (alpha is None): alpha = 1
        self.alpha = alpha
        self.method = method
        self.pos = pos
        self.EXCESS_MAD_CONSTANTS = {
            'first_two': 158.8,  # First-two-digits test (90 categories, k=10..99)
            1: 21.27,            # First digit test (9 categories, k=1..9)
            2: 30.30,            # Second digit test (10 categories, k=0..9)
            3: 31.83,            # Third digit test (10 categories, approximately uniform)
        }
        self.verbose = verbose

        # Benford's Law percentage-distribution for leading digits
        if pos == 'first_two':
            # First-two-digits test: 90 categories (10-99)
            # Probabilities from Benford's Law: log10(1 + 1/k) for k=10..99
            self.leading_digits = np.array([math.log(1 + (1 / k), 10) for k in range(10, 100)]) * 100
            self.digit_range = range(10, 100)
        elif pos == 1:
            self.leading_digits = np.array(list(map(lambda x: math.log(1 + (1 / x), 10), np.arange(1, 10)))) * 100
            self.digit_range = range(1, 10)
        elif pos == 2:
            self.leading_digits = [12, 11.4, 10.9, 10.4, 10, 9.7, 9.3, 9, 8.8, 8.5]
            self.digit_range = range(0, 10)
        elif pos == 3:
            self.leading_digits = [10.2, 10.1, 10.1, 10.1, 10.0, 10.0, 9.9, 9.9, 9.9, 9.8]
            self.digit_range = range(0, 10)
        elif pos == 0:
            logger.error("There is no leading digit distribution for the 0 digit!")
            raise ValueError("There is no leading digit distribution for the 0 digit!")
        elif isinstance(pos, int) and (pos > 3 or pos < 0):
            logger.info(f'[benfordslaw] >The is no leading digit distribution explicitly specified for digit [{pos}] and therefore the Uniform distribution is used instead.')
            # Approximation, near-uniform distribution
            self.leading_digits = [10.0] * 10
            self.digit_range = range(0, 10)

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
           3. Dataset should preferably cover at least 1000 samples. Though Benford's law has been shown to hold true for datasets containing as few as 50 numbers.

        Parameters
        ----------
        X : list or numpy array
            Input data.

        Examples
        --------
        >>> # Import library
        >>> from benfordslaw import benfordslaw
        >>> #
        >>> # Initialize with MAD method
        >>> bl = benfordslaw(pos='first_two', method='mad')
        >>> #
        >>> # Get data for one candidate
        >>> df = bl.import_example()
        >>> X = df['votes'].loc[df['candidate']=='Donald Trump'].values
        >>> #
        >>> # Fit
        >>> results = bl.fit(X)
        >>> #
        >>> # Access Excess MAD (negative values indicate conformity to Benford's Law)
        >>> print(f"Excess MAD: {results['excess_mad']}")
        >>> #
        >>> # Figure
        >>> fig, ax = bl.plot()

        Returns
        -------
        dict containing:
            P : float
                P-value from the statistical test (NaN for MAD method).
            t : float
                Test statistic (Excess MAD for MAD method).
            P_significant : bool
                Whether the result is significant at alpha level.
            percentage_emp : ndarray
                Empirical digit frequencies.
            mad : float
                Mean Absolute Deviation from Benford's Law.
            expected_mad : float
                Expected MAD for a pure Benford set of the same size.
            excess_mad : float
                Excess MAD = MAD - E(MAD). Negative values indicate conformity,
                positive values indicate deviation from Benford's Law.
            conformity_mad : str
                Conformity assessment based on MAD thresholds ('close conformity',
                'acceptable conformity', 'marginally acceptable conformity', or 'nonconforming').
            N : int
                Number of observations used in the analysis.

        References
        ----------
        * Barney, B. J., & Schulzke, K. S. (2016). Moderating "Cry Wolf" Events with Excess MAD
          in Benford's Law Research and Practice. Journal of Forensic Accounting Research, 1(1), A66-A90.
        * Nigrini, M. (2012). Benford's Law: Applications for Forensic Accounting, Auditing, and
          Fraud Detection. Hoboken, NJ: John Wiley & Sons.

        """
        # Make distribution first digits
        logger.info(f"Analyzing digit position: {self.pos}")
        self.results = {}
        # Convert pandas dataframe to numpy array
        if isinstance(X, pd.DataFrame): X = X.values.ravel()
        # Count digit based on position type
        if self.pos == 'first_two':
            counts_emp, percentage_emp, total_count, digit = _count_first_two_digits(X)
        else:
            counts_emp, percentage_emp, total_count, digit = _count_digit(X, self.pos, self.digit_range)
        # Expected counts
        counts_exp = self._get_expected_counts(total_count)

        # Compute MAD and Excess MAD (always computed regardless of method)
        mad, expected_mad, excess_mad, conformity = self._compute_mad_statistics(counts_emp, total_count)

        # Compute Pvalues based on method
        tstats, Praw = np.nan, np.nan
        if total_count > 0:
            if self.method == 'chi2':
                try:
                    tstats, Praw = chisquare(counts_emp, f_exp=counts_exp)
                except:
                    raise Exception('The relative tolerance of the chisquare test is not reached. Try using another method such as "method=ks". This is not a bug but a feature: "https://github.com/scipy/scipy/issues/13362" ')
            elif self.method == 'ks':
                tstats, Praw = ks_2samp(counts_emp, counts_exp)
            elif self.method == 'mad':
                # For MAD method, use excess_mad as the test statistic
                # P-value is not applicable for MAD-based assessment
                tstats = excess_mad
                Praw = np.nan
            else:
                stats1, Praw1 = chisquare(counts_emp, f_exp=counts_exp)
                tstats2, Praw2 = ks_2samp(counts_emp, counts_exp)
                tstats, Praw = combine_pvalues([Praw1, Praw2], method='fisher')
                self.method = 'P_ensemble'

        # Show message
        if self.method == 'mad':
            logger.info(f"[{self.method}] {'No anomaly detected' if excess_mad <= 0 else 'Potential anomaly'}. Excess MAD={excess_mad} ({conformity})")
        elif np.isnan(Praw):
            logger.info("No data available for this position.")
        elif (Praw <= self.alpha):
            logger.info(f"[{self.method}] Anomaly detected! P={Praw}, Tstat={tstats}")
        elif (Praw > self.alpha):
            logger.info(f"[{self.method}] No anomaly detected. P={Praw}, Tstat={tstats}")
        
        # Set bool based on selected method
        if self.method == 'mad':
            self.results['P_significant'] = excess_mad > 0
        else:
            self.results['P_significant'] = Praw <= self.alpha
            
        # Store
        self.results['N'] = int(total_count)
        self.results['P'] = Praw
        self.results['t'] = tstats
        self.results['percentage_emp'] = np.c_[digit, percentage_emp]
        # Always include MAD statistics
        self.results['mad'] = mad
        self.results['expected_mad'] = expected_mad
        self.results['excess_mad'] = excess_mad
        self.results['conformity_mad'] = conformity

        # return
        return self.results

    def _compute_mad_statistics(self, counts_emp, total_count):
        """Compute MAD, Expected MAD, and Excess MAD statistics.

        Mean Absolute Deviation (MAD) measures the average absolute difference between
        observed and expected digit frequencies. Excess MAD adjusts for sample size,
        providing a more reliable measure for detecting anomalies in Benford's Law analysis.

        Parameters
        ----------
        counts_emp : array-like
            Empirical counts for each digit category.
        total_count : int
            Total number of observations.

        Returns
        -------
        mad : float
            Mean Absolute Deviation.
        expected_mad : float
            Expected MAD for a pure Benford set of the same size (E(MAD) ≈ 1/√(C×N)).
        excess_mad : float
            Excess MAD = MAD - E(MAD). Values below 0 indicate conformity.
        conformity : str
            Conformity assessment based on Nigrini (2012) thresholds.

        References
        ----------
        * Nigrini, M. (2012). Benford's Law: Applications for Forensic Accounting,
          Auditing, and Fraud Detection. Hoboken, NJ: John Wiley & Sons.
        * Barney, B. J., & Schulzke, K. S. (2016). Moderating "Cry Wolf" Events with
          Excess MAD in Benford's Law Research and Practice.

        """
        if total_count == 0:
            return np.nan, np.nan, np.nan, 'insufficient data'

        # Calculate observed proportions
        observed_proportions = np.array(counts_emp) / total_count

        # Calculate expected proportions (from leading_digits, which are in percentages)
        expected_proportions = np.array(self.leading_digits) / 100

        # Calculate MAD: mean of absolute deviations
        # MAD = (1/K) × Σ|Obs_k/N - Exp_k|
        K = len(self.leading_digits)
        mad = np.sum(np.abs(observed_proportions - expected_proportions)) / K

        # Calculate Expected MAD for a pure Benford set
        # E(MAD) ≈ 1 / √(C × N) where C depends on the digit test
        C = self._get_excess_mad_constant()
        expected_mad = 1.0 / math.sqrt(C * total_count)

        # Calculate Excess MAD (the key contribution from Barney & Schulzke 2016)
        excess_mad = mad - expected_mad

        # Determine conformity based on Nigrini (2012) thresholds
        # Thresholds are calibrated for the first-two-digits test
        if self.pos == 'first_two':
            # Original thresholds from Nigrini (2012) for first-two-digits test
            if mad < 0.0012:
                conformity = 'close conformity'
            elif mad < 0.0018:
                conformity = 'acceptable conformity'
            elif mad < 0.0022:
                conformity = 'marginally acceptable conformity'
            else:
                conformity = 'nonconforming'
        else:
            # For other digit tests, use Excess MAD-based interpretation
            # Negative Excess MAD indicates better-than-expected conformity
            if excess_mad < 0:
                conformity = 'close conformity'
            elif excess_mad < 0.001:
                conformity = 'acceptable conformity'
            elif excess_mad < 0.002:
                conformity = 'marginally acceptable conformity'
            else:
                conformity = 'nonconforming'

        return mad, expected_mad, excess_mad, conformity

    def _get_excess_mad_constant(self):
        """Get the constant C for Expected MAD calculation.

        The constant C is derived from the variance of the binomial distribution
        for each digit test type. For the first-two-digits test, C = 158.8 as
        derived in Barney & Schulzke (2016).

        The formula for C is:
        C = K² × π / (2 × (Σ √(p_k × (1 - p_k)))²)

        where K is the number of digit categories and p_k are the Benford probabilities.

        Returns
        -------
        float
            The constant C for the current digit test.

        References
        ----------
        * Barney, B. J., & Schulzke, K. S. (2016). Moderating "Cry Wolf" Events with
          Excess MAD in Benford's Law Research and Practice.

        """
        if self.pos == 'first_two':
            return self.EXCESS_MAD_CONSTANTS['first_two']
        elif self.pos in self.EXCESS_MAD_CONSTANTS:
            return self.EXCESS_MAD_CONSTANTS[self.pos]
        else:
            # For other positions, use an approximation based on the distribution
            # C ≈ K² × π / 2 for approximately uniform distributions
            K = len(self.leading_digits)
            return K * K * math.pi / 2

    # Plot
    def plot(self, title='', fontsize=16, barcolor='black', barwidth=0.3, label='Empirical distribution', figsize=(15, 8), grid=True):
        """Make bar chart of observed vs expected digit frequency in percent.

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
        # attach a text label above each bar displaying its height
        for rect, perc in zip(rects1, data_percentage[:, 1]):
            if not np.isnan(perc):
                height = rect.get_height()
                # Only show labels for first digit or first_two with limited labels
                if self.pos != 'first_two':
                    ax.text(rect.get_x() + rect.get_width() / 2, height, '{:0.1f}%'.format(height), ha='center', va='bottom', fontsize=13)

        # Plot expected benfords values
        ax.scatter(x, self.leading_digits, s=150 if self.pos != 'first_two' else 30, c='red', zorder=2, label='Benfords distribution')

        # Build title based on method
        if self.method == 'mad':
            title = title + "\nExcess MAD=%g (%s)" % (self.results['excess_mad'], self.results['conformity_mad'])
        elif not np.isnan(self.results['P']) and self.results['P'] <= self.alpha:
            title = title + "\nAnomaly detected! P=%g, Tstat=%g" % (self.results['P'], self.results['t'])
        elif not np.isnan(self.results['P']):
            title = title + "\nNo anomaly detected. P=%g, Tstat=%g" % (self.results['P'], self.results['t'])

        # Add MAD info to title if available
        if 'mad' in self.results and self.method != 'mad':
            title = title + "\nMAD=%g, Excess MAD=%g" % (self.results['mad'], self.results['excess_mad'])

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_title(title, fontsize=fontsize)
        ax.set_ylabel('Frequency (%)', fontsize=fontsize)
        ax.set_xlabel('Digits', fontsize=fontsize)

        # Adjust x-axis for first_two digits test
        if self.pos == 'first_two':
            # Show fewer tick labels for readability
            tick_positions = list(range(10, 100, 10))
            ax.set_xticks(tick_positions)
            ax.set_xticklabels(tick_positions, fontsize=fontsize - 2)
        else:
            ax.set_xticks(x.astype(int))
            ax.set_xticklabels(x.astype(int), fontsize=fontsize)

        if grid:
            ax.grid(True, which='both', linestyle='--', linewidth=0.9, alpha=0.8)

        # Hide the right and top spines & add legend
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.legend(prop={'size': 15}, frameon=False)
        ax.legend()

        plt.show()
        return fig, ax

    def import_example(self, data='elections', url=None, sep=',', verbose='info'):
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

        return dz.get(data=data, url=url, sep=sep, verbose=verbose)

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
    data = data[data >= 1]

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


# %% Counts and the frequencies in percentage for the first two digits
def _count_first_two_digits(data):
    """Count the first two digits of each number in the data.

    Parameters
    ----------
    data : array-like
        Input data containing numbers.

    Returns
    -------
    empirical_counts : ndarray
        Counts for each first-two-digit pair (10-99).
    empirical_percentage : list
        Percentage for each first-two-digit pair.
    total_count : int
        Total number of valid observations.
    digit : list
        List of digit pairs (10-99).

    """
    # Convert to numpy array if needed
    data = np.asarray(data).flatten()

    # Get only values with at least 2 digits (>= 10)
    data = data[data >= 10]

    # Get the first two digits
    first_two_digits = []
    for x in data:
        s = str(int(abs(x)))
        if len(s) >= 2:
            first_two_digits.append(int(s[:2]))

    # Count occurences for each pair from 10 to 99
    empirical_counts = np.zeros(90)
    digit = []
    for i in range(10, 100):
        empirical_counts[i - 10] = first_two_digits.count(i)
        digit.append(i)

    # Total amount
    total_count = sum(empirical_counts)
    empirical_percentage = [np.nan] * len(empirical_counts)

    # Make percentage
    if total_count > 0:
        empirical_percentage = [(i / total_count) * 100 for i in empirical_counts]

    # Return
    return empirical_counts, empirical_percentage, total_count, digit


# %% Counts and the frequencies in percentage for the second digit
def _count_digit(data, d, digit_range):
    # Get only non-zero values
    data = data[data >= 1]

    # Reverse numbers if last digits is required
    if d < 0:
        data = list(map(lambda x: x[::-1], data.astype(str)))
        data = np.array(data).astype(int)
        d = d * -1

    # Remove one because pythons starts counting from 0
    d = d - 1

    # Get the ith digit
    digits = np.zeros_like(data)
    Iloc = data >= np.power(10, d)
    Iloc[np.isnan(Iloc)] = False
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
    empirical_percentage = [np.nan] * len(empirical_counts)
    # Make percentage
    if total_count > 0:
        empirical_percentage = [(i / total_count) * 100 for i in empirical_counts]
    # Return
    return empirical_counts, empirical_percentage, total_count, digitnr


# %% Standalone function for computing Excess MAD
def compute_excess_mad(data, pos='first_two'):
    """Compute Excess MAD for a dataset without creating a benfordslaw object.

    This is a convenience function that computes the Excess MAD statistic
    directly, which is useful for quick assessments of Benford's Law conformity.

    Parameters
    ----------
    data : array-like
        Input data containing numbers.
    pos : str or int, (default: 'first_two')
        Digit position to analyze. See benfordslaw class for options.

    Returns
    -------
    dict containing:
        mad : float
            Mean Absolute Deviation.
        expected_mad : float
            Expected MAD for a pure Benford set.
        excess_mad : float
            Excess MAD (MAD - E(MAD)).
        conformity : str
            Conformity assessment.
        N : int
            Number of observations.

    Examples
    --------
    >>> from benfordslaw import compute_excess_mad
    >>> data = [123, 456, 789, 1011, 1213]
    >>> result = compute_excess_mad(data, pos='first_two')
    >>> print(f"Excess MAD: {result['excess_mad']}")

    References
    ----------
    * Barney, B. J., & Schulzke, K. S. (2016). Moderating "Cry Wolf" Events with Excess MAD
      in Benford's Law Research and Practice. Journal of Forensic Accounting Research, 1(1), A66-A90.

    """
    bl = benfordslaw(pos=pos, method='mad', verbose='info')
    results = bl.fit(np.asarray(data))
    return {
        'mad': results['mad'],
        'expected_mad': results['expected_mad'],
        'excess_mad': results['excess_mad'],
        'conformity_mad': results['conformity_mad'],
        'N': results['N']
    }



# %%
def set_logger(verbose: [str, int] = 'info', return_status: bool = False):
    """Set the logger for verbosity messages.

    Parameters
    ----------
    verbose : [str, int], default is 'info' or 20
        Set the verbose messages using string or integer values.
            * 0, 60, None, 'silent', 'off', 'no']: No message.
            * 10, 'debug': Messages from debug level and higher.
            * 20, 'info': Messages from info level and higher.
            * 30, 'warning': Messages from warning level and higher.
            * 50, 'critical': Messages from critical level and higher.

    Returns
    -------
    None.

    Examples
    --------
    >>> # Set the logger to warning
    >>> set_logger(verbose='warning')
    >>>
    >>> # Test with different messages
    >>> logger.debug("Hello debug")
    >>> logger.info("Hello info")
    >>> logger.warning("Hello warning")
    >>> logger.critical("Hello critical")
    >>>
    """
    # Set 0 and None as no messages.
    if (verbose==0) or (verbose is None):
        verbose=60
    # Convert str to levels
    if isinstance(verbose, str):
        levels = {
            'silent': logging.CRITICAL + 10,
            'off': logging.CRITICAL + 10,
            'no': logging.CRITICAL + 10,
            'debug': logging.DEBUG,
            'info': logging.INFO,
            'warning': logging.WARNING,
            'error': logging.ERROR,
            'critical': logging.CRITICAL,
        }
        verbose = levels[verbose]

    # Show examples
    logger.setLevel(verbose)
    if return_status:
        return verbose


# %%
def get_logger():
    return logger.getEffectiveLevel()


# %% Main
if __name__ == "__main__":
    logger.info(f'Please bootup python and run benfordslaw as described in the readme file: https://github.com/erdogant/benfordslaw')

