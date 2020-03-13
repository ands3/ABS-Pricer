'''
Andy Zhang
1/6/2020
Exercise 2.2.1: Script for derived Loan classes.
'''

# using Loan class
from loan_base import Loan

'''=================================================
FixedRateLoan and VariableRateLoan classes:
This module contains the FixedRateLoan and VariableRateLoan classes.
================================================='''
# 2.2.1 a
class FixedRateLoan(Loan):
    '''
    Class to model FixedRateLoan object.

    Methods
    =======
    __init__ :
        initialize all object variables
    getRate :
        return annual interest rate of loan given period
    '''

    # 2.2.7
    def __init__(self, asset, term, rate, face):
        '''
        Initialize variables.
        '''
        # check that rate input is valid
        # rate input is not a positive number
        if not (type(rate) is float and rate > 0):
            print 'Annual interest rate should be a positive number.'
        # rate input is valid
        else:
            super(FixedRateLoan, self).__init__(asset, term, rate, face)

    def getRate(self, period):
        '''
        Return the annualized interest rate for the given period.
        '''
        # Overrides the base Loan class

        # period is not a nonnegative integer
        if not (type(period) is int and period >= 0):
            # error message
            print 'The period must be a nonnegative integer.'
            return

        # annualized interest rate
        return self._rate

# 2.2.1 b
class VariableRateLoan(Loan):
    '''
    Class to model VariableRateLoan object.

    Parameters
    ==========
    _rateDict : dict of int:float
        dict of variable interest rates for range of periods

    Methods
    =======
    __init__ :
        initialize all object variables
    getRate :
        return annual interest rate of loan given period
    '''

    def __init__(self, term, rateDict, face):
        '''
        Initialize variables.
        '''
        # initialization
        self._rateDict = None

        # check that rateDict input is valid
        # rateDict is not a dict of int:float
        # 1) not a dict or 2) non-int keys or 3) non-float values or 4) int keys aren't from smallest to largest or
        # 5) smallest key not 0 or 6) smallest value (i.e. rate) is nonpositive
        if type(rateDict) is not dict or all(type(k) is not int for k in rateDict.keys()) or \
                all(type(v) is not float for v in rateDict.values()) or rateDict.keys() != sorted(rateDict.keys()) or \
                min(rateDict.keys()) != 0 or min(rateDict.values()) <= 0:
            print 'rateDict should be a dict of int:float, with starting key being 0, keys going from smallest to ' \
                  'largest, and all values being positive.'
        # rateDict input is valid
        else:
            self._rateDict = rateDict

            # rate is set to None because we have a rateDict
            super(VariableRateLoan, self).__init__(term, None, face)

    def getRate(self, period):
        '''
        Return the annualized interest rate for the given period.
        '''
        # Overrides the base Loan class

        # period is not a nonnegative integer
        if not (type(period) is int and period >= 0):
            # error message
            print 'The period must be a nonnegative integer.'
            return

        # Getting the appropriate rate requires finding the last key for which period is greater than or equal to. This
        # is equivalent to finding the first key of the reversed list of keys for which period is greater than or equal
        # to.
        # First sort rateDict's list of keys in reverse order. Next, loop through them.
        for k in sorted(self._rateDict.keys(), reverse=True):
            # Find first key that period is greater than or equal to
            if period >= k:
                # Get corresponding rateDict value
                return self._rateDict[k]
