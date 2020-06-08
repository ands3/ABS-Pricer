'''
Andy Zhang
2/17/2020
Case Study: Script for the LoanPool class
'''

from level5_5_2_2_to_5_2_3.loans import FixedRateLoan  # using FixedRateLoan class
from level3_3_2_3.global_functions import WeightedAverageMaturity, WeightedAverageRate  # using WAM and WAR
import random  # using random module
import time  # using time module

# set seed
random.seed(time.time())

'''=================================================
LoanPool class:
This module contains the LoanPool class.
================================================='''
class LoanPool(object):
    '''
    Class to model LoanPool object.

    Parameters
    ==========
    _loan_active : list of int
        list of each loan's total period of activity (in months)
    _loan_pool : tuple / list of FixedRateLoan objects
        pool of loans
    _loan_ids : list of int
        list of each loan's ID
    _idx : int
        indexing for LoanPool iterable

    Methods
    =======
    __init__ method :
        initialize all object variables
    __iter__ method :
        return iterator object itself
    next method :
        return next item in LoanPool iterator
    reset_index method:
        reset _idx back to 0
    @property loan_pool :
        get pool of loans
    @loan_pool.setter loan_pool :
        set pool of loans
    @property loan_active :
        get list of loans' period of activity up to current period
    @loan_pool.setter loan_pool :
        set list of loan's period of activity up to current period
    @property loan_ids :
        get list of loan IDs
    totalLoanPrincipal :
        return total loan principal
    totalLoanBalance :
        return total loan principal at a given period
    aggPrincipalDue :
        return aggregate principal due at a given period
    aggInterestDue :
        return aggregate interest due at a given period
    aggTotalPmtDue :
        return aggregate total payment due at a given period
    numActiveLoans :
        return the number of 'active' loans, i.e., loans with positive balance, at a given period
    WAM :
        return the weighted average maturity (WAM) of the loans
    WAR :
        return the weighted average rate (WAR) of the loans
    getWaterfall :
        return list of lists containing Principal Due, Interest Due, and Loan Balance for each loan for a given time
        period
    checkDefaults :
        generate a uniform random integer for each loan that has the same odds as the default probability for the given
        time period and then call each loan's checkDefault() method with the generated uniform random integer.
    '''

    # Case Study
    #########

    def __init__(self, loan_active, loan_ids, *args):
        '''
        Initialize variables.
        '''
        # initialization
        self._loan_active = None  # list of each loan's period of activity (in months)
        self._loan_pool = None  # pool of Loan objects
        self._loan_ids = None  # list of loan IDs
        self._idx = 0  # indexing for LoanPool iterable

        # check that inputs are valid
        # loan_active is not a list of nonnegative int
        if type(loan_active) is not list or not all(type(ln) is int and ln >= 0 for ln in loan_active):
            print('loan_active needs to be a list of nonnegative int.')
        # args is not a tuple / list of Loan objects and/or the rates in the Loan objects is None
        elif not all(isinstance(ln, FixedRateLoan) for ln in args):
            print('args input needs to be a tuple / list of Loan objects.')
        # loan_ids is not a list of unique ints
        elif type(loan_ids) is not list or not all(type(ln) is int for ln in loan_ids) or \
                len(loan_ids) != len(set(loan_ids)):
            print('loan_ids needs to be a list of unique int.')
        # loan_active, args, and loan_ids are not of the same size
        elif len(loan_active) != len(args) or len(loan_active) != len(loan_ids) or len(loan_ids) != len(args):
            print('loan_active, args, and loan_ids need to be of the same size.')
        # inputs are valid
        else:
            self._loan_active = loan_active
            self._loan_pool = args
            self._loan_ids = loan_ids

    # level3_3_2_3
    #############

    def __iter__(self):
        '''
        Return iterator object itself.
        '''
        return self

    # Python 2 uses next() whereas Python 3 uses __next__()
    # cf. https://stackoverflow.com/questions/21665485/how-to-make-a-custom-object-iterable
    def __next__(self):
        '''
        Return next item in LoanPool iterator.
        '''
        # increment index by 1 to move to next item in list
        self._idx += 1
        try:
            return self._loan_pool[self._idx-1]
        # index out of range, i.e., greater than last index of list
        except IndexError:
            # reset idx to 0
            self._idx = 0
            # no more items to read
            raise StopIteration

    def reset_index(self):
        '''
        Reset _idx back to 0.
        '''
        self._idx = 0

    # getters/setters

    @property
    def loan_pool(self):
        '''
        Return LoanPool object.
        '''
        return self._loan_pool

    @loan_pool.setter
    def loan_pool(self, iloan_pool):
        '''
        Set LoanPool object.
        '''
        # iloan_pool is not a tuple / list of Loan objects
        if not all(isinstance(ln, FixedRateLoan) for ln in iloan_pool):
            # error message
            print('The loan pool must be a tuple / list of Loan objects.')
        # iloan_pool valid
        else:
            self._loan_pool = iloan_pool

    @property
    def loan_active(self):
        '''
        Return the list of loans' period of activity up to current period.
        '''
        return self._loan_active

    @loan_active.setter
    def loan_active(self, iloan_active):
        '''
        Set the list of loans' period of activity up to current period.
        '''
        # iloan_active is not a list of int
        if type(iloan_active) is not list or not all(type(ln) is int and ln >= 0 for ln in iloan_active):
            # error message
            print('The list of each loan\'s period of activity must be a list of nonnegative int.')
        # iloan_active valid
        else:
            self._loan_active = iloan_active

    # Case Study
    ###########

    @property
    def loan_ids(self):
        '''
        Return the list of loan IDs.
        '''
        return self._loan_ids

    # 2.2.5 a
    #############

    def totalLoanPrincipal(self):
        '''
        Return the total loan principal.
        '''
        # total loan principal
        return sum(ln.face for ln in self._loan_pool)

    # 2.2.5 b
    #############

    def totalLoanBalance(self, period):
        '''
        Return the total balance of all loans in the loan pool at the time of the given period.
        '''
        # period is not a nonnegative integer
        if not (type(period) is int and period > 0):
            # error message
            print('The period must be a nonnegative integer.')
            return

        # total loan balance in period
        return sum(ln.balance_formula(period + active) for active, ln in zip(self._loan_active, self._loan_pool))

    # Case Study (previously 2.2.5 c)
    #############

    def aggPrincipalDue(self, period):
        '''
        Return aggregate principal due of all loans in the loan pool in the given period.
        '''
        # period is not a nonnegative integer
        if not (type(period) is int and period >= 0):
            # error message
            print('The period must be a nonnegative integer.')
            return

        # aggregate principal due in period
        return sum(ln.principalDue(period + active) for active, ln in zip(self._loan_active, self._loan_pool))

    # Case Study
    #########

    def aggInterestDue(self, period):
        '''
        Return aggregate interest due of all loans in the loan pool in the given period.
        '''
        # period is not a nonnegative integer
        if not (type(period) is int and period >= 0):
            # error message
            print('The period must be a nonnegative integer.')
            return

        # aggregate interest due in period
        return sum(ln.interestDue_formula(period + active) for active, ln in zip(self._loan_active, self._loan_pool))

    # Case Study
    #########

    def aggTotalPmtDue(self, period):
        '''
        Return aggregate total payment due of all loans in the loan pool in the given period.
        '''
        # period is not a nonnegative integer
        if not (type(period) is int and period >= 0):
            # error message
            print('The period must be a nonnegative integer.')
            return

        # aggregate total payment due in period
        return self.aggInterestDue(period) + self.aggPrincipalDue(period)

    # 2.2.5 d
    #############

    def numActiveLoans(self):
        '''
        Return the number of 'active' loans.
        '''
        # number of 'active' loans
        return sum(ln.balance_formula(active) > 0.0 for active, ln in zip(self._loan_active, self._loan_pool))

    # 2.2.5 e
    #############

    def WAM(self):
        '''
        Return the Weighted Average Maturity (WAM) of the loans in the loan pool.
        '''
        # get mortgage terms to be used in Weighted Average Maturity (WAM) global function
        mortgage_terms = [(ln.face, ln.rate, ln.term) for ln in self._loan_pool]

        # get WAM
        return WeightedAverageMaturity(mortgage_terms)

    def WAR(self):
        '''
        Return the Weighted Average Rate (WAR) of the loans in the loan pool.
        '''
        # get mortgage terms to be used in Weighted Average Rate (WAR) global function
        mortgage_terms = [(ln.face, ln.rate, ln.term) for ln in self._loan_pool]

        # get WAR
        return WeightedAverageRate(mortgage_terms)

    # Case Study
    ###########

    def getWaterfall(self, period):
        '''
        Return list of lists containing Principal Due, Interest Due, and Loan Balance for each loan for a given time
        period.
        '''
        return [[
            # principal due
            ln.principalDue(period + active),
            # interest due
            ln.interestDue_formula(period + active),
            # balance
            ln.balance_formula(period + active)] for ln, active in zip(self._loan_pool, self._loan_active)]

    def checkDefaults(self, period):
        '''
        Generate a uniform random integer for each loan that has the same odds as the default probability for the given
        time period and then call each loan's checkDefault() method with the generated uniform random integer.
        '''
        # aggregate recovery values
        aggRecoveryValues = 0.

        # loop through loans
        for ln, active in zip(self._loan_pool, self._loan_active):
            # dict of default probabilities by last period applicable
            defaultProbByPeriod = {10: .0005, 59: .001, 119: .002, 179: .004, 209: .002, 360: .001}

            # Getting the appropriate default probability requires finding the last key for which period is less than or
            # equal to. This is equivalent to finding the first key of the reversed list of keys for which period is
            # less than or equal to.
            # First sort defaultProbByPeriod's list of keys in reverse order. Next, loop through them.
            for k in sorted(defaultProbByPeriod.keys(), reverse=True):
                # Find first key that period is less than or equal to
                if period + active <= k:
                    # call loan's checkDefault() method
                    aggRecoveryValues += ln.checkDefault(period + active,
                                                         random.randint(0, int(1 / defaultProbByPeriod[k] - 1)))

        return aggRecoveryValues
