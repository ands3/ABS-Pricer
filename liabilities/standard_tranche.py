'''
Andy Zhang
2/14/2020
Case Study: Script for derived Tranche class.
'''

from liabilities.tranche import Tranche  # using Tranche class
import logging  # using logging module

'''=================================================
StandardTranche class:
This module contains the Standard Tranche class.
================================================='''
class StandardTranche(Tranche):
    '''
    Class to model StandardTranche object.

    Parameters
    ==========
    _tranche_percent : float
        tranche percentage
    _period : int
        current time period
    _prinDue : dict of int : float
        dict of each period's principal due
    _prinPmts : dict of int : float
        dict of each period's principal payment
    _interestPmts : dict of int : float
        dict of each period's interest payment
    _prinShortfalls : dict of int : float
        dict of each period's principal shortfall
    _interestShortfalls : dict of int : float
        dict of each period's interest shortfall

    Methods
    =======
    __init__ :
        initialize all object variables
    @property tranchePercent :
        get tranche percent
    @tranchePercent.setter tranchePercent :
        set tranche percent
    @property period :
        get the current time period
    @property prinDue :
        get dict of each recorded period's principal due
    @prinDue.setter prinDue :
        set principal due for a given period
    @property prinPmts :
        get dict of each recorded period's principal payment
    @prinPmts.setter prinPmts :
        set principal payment for a given period
    @property interestPmts :
        get dict of each recorded period's interest payment
    @interestPmts.setter interestPmts :
        set interest payment for a given period
    @property prinShortfalls :
        get dict of each recorded period's principal shortfall
    @prinShortfalls.setter prinShortfalls :
        set principal shortfall for a given period
    @property interestShortfalls :
        get dict of each recorded period's interest shortfall
    @interestShortfalls.setter interestShortfalls :
        set interest shortfall for a given period
    getNotional :
        return the notional
    increaseTimePeriod :
        increase the current time period by 1
    makePrincipalPayment :
        record principal payment for current period
    makeInterestPayment :
        record interest payment for current period
    notionalBalance :
        return the notional still owed for the current period (after any payments made)
    interestDue :
        return the interest due in the current period
    reset :
        reset tranche to its original state (time 0)
    '''

    def __init__(self, notional, rate, subordinate, tranche_percent):
        '''
        Initialize variables.
        '''
        self._tranche_percent = None  # tranche percent
        self._period = 0  # current time period
        self._prinDue = {}  # dict of each period's principal due
        self._prinPmts = {}  # dict of each period's principal payment
        self._interestPmts = {}  # dict of each period's interest payment
        self._prinShortfalls = {-1: 0}  # dict of each period's principal shortfall
        self._interestShortfalls = {-1: 0}  # dict of each period's interest shortfall

        # Check if tranche percent is valid. Other inputs will be checked from the call to Tranche class via super().
        # tranche percent is not a positive number
        if not (type(tranche_percent) is float and tranche_percent > 0):
            raise TypeError('Tranche percent should be a positive number.')
        # tranche_percent is valid
        else:
            self._tranche_percent = tranche_percent

            super(StandardTranche, self).__init__(notional, rate, subordinate)

    # getters/setters

    @property
    def tranchePercent(self):
        '''
        Return the tranche percent.
        '''
        return self._tranche_percent

    @tranchePercent.setter
    def tranchePercent(self, itranche_percent):
        '''
        Set the tranche percent.
        '''
        # check itranche_percent is valid
        # itranche_percent is not a positive number
        if not (type(itranche_percent) is float and itranche_percent > 0):
            raise ValueError('itranche_percent should be a positive number.')
        # itranche_percent is valid
        else:
            self._tranche_percent = itranche_percent

    @property
    def period(self):
        '''
        Return the current time period.
        '''
        return self._period

    @property
    def prinDue(self):
        '''
        Return dict of each recorded period's principal due.
        '''
        return self._prinDue

    @prinDue.setter
    def prinDue(self, principal_due, period):
        '''
        Set principal due for a given period.
        '''
        # check if the inputs are valid
        # period is a positive int
        if not (type(period) is int and period > 0):
            raise ValueError('period should be a positive integer.')
        # principal due already recorded this period
        elif period in self._prinDue:
            raise Exception(f'The principal due for period {period} has already been recorded.')
        # principal due this period not recorded yet
        else:
            self._prinDue[period] = principal_due

    @property
    def prinPmts(self):
        '''
        Return dict of each recorded period's principal payment.
        '''
        return self._prinPmts

    @prinPmts.setter
    def prinPmts(self, principal_pmt, period):
        '''
        Set principal payment for a given period.
        '''
        # check if inputs are valid
        # period is a positive int
        if not (type(period) is int and period > 0):
            raise ValueError('period should be a positive integer.')
        # principal payment already made this period
        elif period in self._prinPmts:
            raise Exception(f'The principal payment for period {period} has already been made.')
        # principal payment hasn't been made this period
        else:
            self._prinPmts[period] = principal_pmt

    @property
    def interestPmts(self):
        '''
        Return dict of each recorded period's interest payment.
        '''
        return self._interestPmts

    @interestPmts.setter
    def interestPmts(self, interest_pmt, period):
        '''
        Set interest payment for a given period.
        '''
        # check if inputs are valid
        # period is a positive int
        if not (type(period) is int and period > 0):
            raise ValueError('period should be a positive integer.')
        # interest payment already made this period
        elif period in self._interestPmts:
            raise Exception(f'The interest payment for period {period} has already been made.')
        # interest payment hasn't been made this period
        else:
            self._interestPmts[period] = interest_pmt

    @property
    def prinShortfalls(self):
        '''
        Return dict of each recorded period's principal shortfall.
        '''
        return self._prinShortfalls

    @prinShortfalls.setter
    def prinShortfalls(self, principal_shortfall, period):
        '''
        Set principal shortfall for a given period.
        '''
        # check if inputs are valid
        # period is a positive int
        if not (type(period) is int and period > 0):
            raise ValueError('period should be a positive integer.')
        # principal shortfall already recorded this period
        elif period in self._prinShortfalls:
            raise Exception(f'The principal shortfall for period {period} has already been recorded.')
        # principal shortfall hasn't been recorded this period
        else:
            self._prinShortfalls[period] = principal_shortfall

    @property
    def interestShortfalls(self):
        '''
        Return dict of each recorded period's interest shortfall.
        '''
        return self._interestShortfalls

    @interestShortfalls.setter
    def interestShortfalls(self, interest_shortfall, period):
        '''
        Set interest shortfall for a given period.
        '''
        # check if inputs are valid
        # period is a positive int
        if not (type(period) is int and period > 0):
            raise ValueError('period should be a positive integer.')
        # interest shortfall already recorded this period
        elif period in self._interestShortfalls:
            raise Exception(f'The interest shortfall for period {period} has already been recorded.')
        # interest shortfall hasn't been recorded this period
        else:
            self._interestShortfalls[period] = interest_shortfall

    def getNotional(self):
        '''
        Return the notional of tranche.
        '''
        # Overrides the base Loan class

        return self._notional

    def increaseTimePeriod(self):
        '''
        Increase the current time period by 1.
        '''
        self._period += 1

    def makePrincipalPayment(self, principal_due, principal_pmt, period):
        '''
        Record principal payment for current time period.
        '''
        # check that inputs are valid
        # principal_due is not a positive number
        if not (type(principal_due) is int and principal_due >= 0 or type(principal_due) is float and
                principal_due >= 0):
            raise ValueError('Principal due needs to be a nonnegative number.')
        # principal_pmt is not a positive number
        elif not (type(principal_pmt) is int and principal_pmt >= 0 or type(principal_pmt) is float and
                  principal_pmt >= 0):
            raise ValueError('Principal payment needs to be a nonnegative number.')
        # period is not a nonnegative int
        elif not (type(period) is int and period >= 0):
            raise ValueError('Period should be a nonnegative number.')
        # inputs valid
        else:
            # check if current notional balance is 0 (in period greater than 0)
            # current notional balance is 0 and period is greater than 0
            if self.notionalBalance(period - 1) == 0 and period > 0:
                raise Exception('The current notional balance is 0, so no more payments necessary.')
            # current notional balance is greater than 0
            else:
                # check if principal payment already made for this period
                # principal payment already made this period
                if period in self._prinPmts:
                    raise Exception('The principal payment for period {period} has already been made.')
                # principal payment hasn't been made this period
                else:
                    if period == 0:
                        # principal payment this period
                        self._prinPmts[period] = 0.
                        # principal shortfall this period
                        self._prinShortfalls[period] = 0.
                    else:
                        # principal payment this period
                        self._prinPmts[period] = principal_pmt
                        # principal shortfall this period
                        self._prinShortfalls[period] = principal_due - principal_pmt
                    self._prinDue[period] = principal_due

    def makeInterestPayment(self, interest_due, interest_pmt, period):
        '''
        Record interest payment for current time period.
        '''
        # check that inputs are valid
        # interest_due is not a positive number
        if not (type(interest_due) is int and interest_due >= 0 or type(interest_due) is float and interest_due >= 0):
            raise ValueError('Interest due needs to be a nonnegative number.')
        # interest_pmt is not a positive number
        elif not (type(interest_pmt) is int and interest_pmt >= 0 or type(interest_pmt) is float and interest_pmt >= 0):
            raise ValueError('Interest payment needs to be a nonnegative number.')
        # period is not a nonnegative int
        elif not (type(period) is int and period >= 0):
            raise ValueError('Period should be a nonnegative number.')
        # inputs valid
        else:
            # check if current interest due is 0 (in period is greater than 0)
            # current interest due is 0 and period is greater than 0
            if interest_due == 0 and period > 0:
                raise Exception('The current interest due is 0, so no more payments necessary.')
            # otherwise
            else:
                # check if interest payment already made for this period
                # interest payment already made this period
                if period in self._interestPmts:
                    raise Exception(f'The interest payment for period {period} has already been made.')
                # interest payment hasn't been made this period
                else:
                    if period == 0:
                        # interest payment this period
                        self._interestPmts[period] = 0.
                        # interest shortfall this period
                        self._interestShortfalls[period] = 0.
                    else:
                        # interest payment this period
                        self._interestPmts[period] = interest_pmt
                        # interest shortfall this period
                        self._interestShortfalls[period] = interest_due - interest_pmt

    def notionalBalance(self, period):
        '''
        Return the notional amount still owed to the tranche for the current period (after any payments made).
        '''
        # total principal payments made up to and including current period
        total_prin_pmts = sum(v for k, v in self._prinPmts.items() if k <= period)

        # period is 0
        if period == 0:
            return self._notional
        # period greater than 0
        else:
            logging.debug(f'notionalBalance() method computes the notional amount still owed for period {period} (after'
                          f' any payments have been made) as the initial tranche balance of {self._notional} minus total'
                          f' principal payments of {total_prin_pmts} plus current principal shortfall of '
                          f'{self._prinShortfalls[period]}')
            # Note: Mark clarified that it is principal shortfall that is considered and not interest shortfall as the
            # Case Study had originally said
            return self._notional - total_prin_pmts + self._prinShortfalls[period]

    def interestDue(self, period):
        '''
        Return the interest due for the current period.
        '''
        # check that input is valid
        # period is not a nonnegative int
        if not (type(period) is int and period >= 0):
            raise ValueError('Period should be a nonnegative integer.')
        # input valid
        else:
            # period is 0
            if period == 0:
                return 0.
            # period greater than 0
            else:
                logging.debug(f'interestDue() method compute the interest due for period {period} as the tranche balance'
                              f' at the beginning of period {period} of {self.notionalBalance(period - 1)} times the '
                              f'annual rate of {self._rate} divided by 12.')
                return self.notionalBalance(period - 1) * self._rate / 12

    def reset(self):
        '''
        Reset tranche to original state.
        '''
        self._period = 0
        self._prinDue = {}
        self._prinPmts = {}
        self._interestPmts = {}
        self._prinShortfalls = {-1: 0}
        self._interestShortfalls = {-1: 0}
