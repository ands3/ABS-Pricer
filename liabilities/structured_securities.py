'''
Andy Zhang
2/17/2020
Case Study: Script for the StructuredSecurities class
'''

from liabilities.standard_tranche import StandardTranche  # using StandardTranche class
from level3_3_2_3.loan_pool import LoanPool  # using LoanPool class

'''=================================================
StructuredSecurities class:
This module contains the StructuredSecurities class.
================================================='''
class StructuredSecurities(object):
    '''
    Class to model StructuredSecurities object.

    Parameters
    ==========
    _totalNotional : float / int
        total notional amount of all StandardTranche objects
    _tranche_list : list of StandardTranche objects
        list of StandardTranche objects
    _subordination_list : list of str
        list of subordination levels
    _mode : str
        one of 'sequential' or 'pro rata' modes for determining principal due
    _reserve_account : float
        leftover cash after making interest and principal payments in a period
    _prinCollections : list of float
        list of each period's principal collections
    _idx : int
        indexing for StructuredSecurities iterable
    _relaxation_coefs :
        list of tranche's relaxation coefficients to be used for relaxation technique

    Methods
    =======
    __init__ method :
        initialize all object variables
    __iter__ method :
        return iterator object itself
    next method :
        return next item in StructuredSecurities iterator
    reset_index method:
        reset _idx back to 0
    @property total_notional :
        get total notional amount
    @total_notional.setter total_notional :
        set total notional amount
    @property tranche_list :
        get list of StandardTranche objects
    @tranche_list.setter tranche_list :
        set list of StandardTranche objects
    @property subordination_levels :
        get the list of subordination levels
    @property reserve_account :
        get the reserve account amount for the period
    @property relaxation_coefs :
        get the list of tranche's relaxation coefficients
    addTranche :
        instantiate and add tranche to internal list of tranches
    modeForPrincipalDue :
        select approach, 'Sequential' or 'Pro Rata', for determining principal due
    increaseTimePeriodOfTranches :
        increase current time period for all tranches
    makePayments :
        cycle through tranches, in order of subordination, and pay off interest and then repeat for principal
    getWaterfall :
        return list of lists containing Interest Due, Interest Paid, Interest Shortfall, Principal Paid, and Balance for
        each tranche for a given time period
    '''

    def __init__(self, total_notional, mode):
        '''
        Initialize variables.
        '''
        # initialization
        self._totalNotional = None  # total notional amount
        self._tranche_list = []  # list of Tranche objects
        self._subordination_levels = []  # list of subordination levels
        self._mode = None  # approach for determining principal due to each tranche
        self._reserve_account = 0  # reserve account amount
        self._prinCollections = []  # list of each period's principal collections
        self._idx = 0  # indexing for StructuredSecurities iterable
        self._relaxation_coefs = []  # list of each tranche's relaxation coefficient

        # check that inputs are valid
        # total notional amount is not a positive number
        if not (type(total_notional) is int and total_notional > 0 or type(total_notional) is float and
                total_notional > 0):
            raise ValueError('The total notional is not a positive number.')
        # check that mode is one of 'sequential' or 'pro rata'
        elif mode not in ['sequential', 'pro rata']:
            raise ValueError('The mode for determining principal due given is {mode}. It should be one of '
                             '\'sequential\' or \'pro rate\'.'.format(mode=mode))
        # inputs is valid
        else:
            self._totalNotional = total_notional
            self._mode = mode

    # Part 2
    #############

    def __iter__(self):
        '''
        Return iterator object itself.
        '''
        return self

    # Python 2 uses next() whereas Python 3 uses __next__()
    # cf. https://stackoverflow.com/questions/21665485/how-to-make-a-custom-object-iterable
    def next(self):
        '''
        Return next item in StructuredSecurities iterator.
        '''
        # increment index by 1 to move to next item in list
        self._idx += 1
        try:
            return self._tranche_list[self._idx - 1]
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
    def total_notional(self):
        '''
        Return the total notional amount.
        '''
        return self._totalNotional

    @total_notional.setter
    def total_notional(self, itotal_notional):
        '''
        Set the total notional amount.
        '''
        # check that itotal_notional input is valid
        # itotal_notional is not a positive number
        if not (type(itotal_notional) is int and itotal_notional <= 0 or type(itotal_notional) is float and
                itotal_notional <= 0):
            raise ValueError('itotal_notional should be a positive number.')
        # itotal_notional is valid
        else:
            self._totalNotional = itotal_notional

    @property
    def tranche_list(self):
        '''
        Return the list of Tranche objects.
        '''
        return self._tranche_list

    @tranche_list.setter
    def tranche_list(self, itranche_list):
        '''
        Set the list of Tranche objects.
        '''
        # check that input is valid
        # itranche_list is not a list of Tranche objects
        if not (type(itranche_list) is list and all(isinstance(tranche, StandardTranche) for tranche in itranche_list)):
            raise TypeError('itranche_list is not a list of StandardTranche objects.')
        # subordination levels are not distinct
        elif len(itranche_list) != len(set(tranche.subordination for tranche in itranche_list)):
            raise Exception('Subordination levels of the StandardTranche objects must be distinct.')
        # itranche_list is valid
        else:
            self._tranche_list = itranche_list

    @property
    def subordination_levels(self):
        '''
        Return the list of subordination levels.
        '''
        return self._subordination_levels

    @property
    def reserve_account(self):
        '''
        Return the reserve account amount for the current period.
        '''
        return self._reserve_account

    @property
    def relaxation_coefs(self):
        '''
        Return the list of each tranche's relaxation coefficient.
        '''
        return self._relaxation_coefs

    def addTranche(self, tranche_class, rate, subordination_level, notional_percent, relaxationCoef):
        '''
        Instantiate and add a tranche to internal list of tranches.
        '''
        # check that inputs are valid
        # tranche_class is not StandardTranche
        if not (type(tranche_class) is str and tranche_class == 'StandardTranche'):
            raise ValueError('tranche_class should be \'StandardTranche\'.')
        # notional_percent is not a positive float
        elif not (type(notional_percent) is float and notional_percent > 0):
            raise ValueError('notional_percent should be a positive float.')
        # rate is not a nonnegative float
        elif not (type(rate) is float and rate >= 0):
            raise ValueError('rate should be a nonnegative float.')
        # subordination_level is not str
        elif type(subordination_level) is not str:
            raise TypeError('subordination_level should be a string.')
        # subordination_level already exists
        elif subordination_level in self._subordination_levels:
            raise Exception('The subordination level given {level} already exists. Please enter a different '
                            'subordination level.'.format(level=subordination_level))
        # relaxation coefficient is not a positive float
        elif not (type(relaxationCoef) is float and relaxationCoef > 0):
            raise ValueError('relaxationCoef should be a positive float.')
        # all inputs valid
        else:
            # append subordination level to list of subordination levels
            self._subordination_levels.append(subordination_level)
            # append relaxation coefficient to list of relaxation coefficients
            self._relaxation_coefs.append(relaxationCoef)
            # StandardTranche object
            tranche = eval(tranche_class)(self._totalNotional * notional_percent, rate, subordination_level,
                                          notional_percent)
            # append tranche to list of tranches
            self._tranche_list.append(tranche)

    def modeForPrincipalDue(self, mode):
        '''
        Select approach, 'Sequential' or 'Pro Rata', for determining principal due.
        '''
        # check if mode input is valid
        # mode is not one of 'sequential' or 'pro rata'
        if mode not in ['sequential', 'pro rata']:
            raise ValueError('The mode given is {mode}. It should be one of \'sequential\' or \'pro rata\'.')
        else:
            # mode is valid
            self._mode = mode

    def increaseTimePeriodOfTranches(self):
        '''
        Increase current time period for all tranches.
        '''
        for tranche in self._tranche_list:
            tranche.increaseTimePeriod()

    def makePayments(self, cash_amount, loan_pool, recoveries):
        '''
        Cycle through tranches, in order of subordination, and pay off interest and then repeat for principal.
        '''
        # check if all inputs are valid
        # cash_amount is not a nonnegative number
        if not (type(cash_amount) is float and cash_amount >= 0 or type(cash_amount) is int and cash_amount >= 0):
            raise ValueError('cash_amount should be a nonnegative number.')
        # loan_pool is not a LoanPool object
        elif not isinstance(loan_pool, LoanPool):
            raise TypeError('loan_pool should be a LoanPool object.')
        # recoveries is not a nonnegative number
        elif not (type(recoveries) is float and recoveries >= 0):
            raise ValueError('Recoveries should be a nonnegative number.')
        # all inputs are valid
        else:
            # sort list of tranches by their subordination levels
            sorted_subordination_levels, sorted_tranche_list = zip(*sorted(zip(self._subordination_levels,
                                                                               self._tranche_list)))

            # get period
            period = sorted_tranche_list[0].period

            # supplement cash_amount with any leftover cash from before
            cash_amount += self._reserve_account

            # get principal collection for period
            prin_collection = loan_pool.aggPrincipalDue(period) + recoveries
            # Get cumulative principal collections. To get this, we first append the principal collection to the list of
            # principal collections. Next, list comprehension is used to get the cumulative sum.
            self._prinCollections.append(prin_collection)
            cum_prin_collections = [sum(self._prinCollections[:i + 1]) for i in range(len(self._prinCollections))]

            # make interest payments in order of subordination
            for tranche in sorted_tranche_list:
                # Interest owed. This is the interest due in the current period plus any interest shortfall incurred
                # from the previous period.
                interest_owed = tranche.interestDue(period) + tranche.interestShortfalls[period - 1]
                # Make payment. Note: This follows from the text "Elements of Structured Finance," which Mark solely
                # recommended for the excellent model itself.
                interest_pmt = min(cash_amount, interest_owed)
                # According to the Case Study, makeInterestPayment() is only called when there is an interest payment to
                # be made. For the purposes of ensuring that calculations are correct, the zero interest payments are
                # also recorded (just not via makeInterestPayment()).
                if interest_pmt > 0:
                    tranche.makeInterestPayment(interest_owed, interest_pmt, period)
                else:
                    tranche.interestPmts[period] = 0
                    tranche.interestShortfalls[period] = interest_owed
                # subtract from available funds
                cash_amount -= interest_pmt

            # make principal payments in order of subordination
            for i, tranche in enumerate(sorted_tranche_list):
                # principal due
                principal_due = 0
                # Note: The formulas given below follow from the text "Elements of Structured Finance" by Ann Rutledge
                # and Sylvain Raynes. The formulas under the 'sequential' approach are slightly more complicated than
                # the formulas under the 'pro rata' approach.
                if self._mode == 'sequential':
                    # first tranche
                    if i == 0:
                        # Note: For more details, please consult "Elements of Structured Finance" by Ann Rutledge and
                        # Sylvain Raynes, page 120.
                        principal_due += min(prin_collection + tranche.prinShortfalls[period - 1],
                                             tranche.notionalBalance(period - 1))
                    # all other tranches
                    else:
                        # Note: For more details, please consult "Elements of Structured Finance" by Ann Rutledge and
                        # Sylvain Raynes, pages 120-121.
                        principal_due += min(
                            max(0, cum_prin_collections[period] -
                                max(sum(t.getNotional() for t in sorted_tranche_list[:i]),
                                    cum_prin_collections[period - 1])) + tranche.prinShortfalls[period - 1],
                            tranche.notionalBalance(period - 1))
                else:
                    principal_due += min(prin_collection * tranche.tranchePercent + tranche.prinShortfalls[period - 1],
                                         tranche.notionalBalance(period - 1))
                # make payment
                principal_pmt = min(cash_amount, principal_due)
                # According to the Case Study, makePrincipalPayment() is only called when there is an interest payment
                # to be made. For the purposes of ensuring that calculations are correct, the zero principal payments
                # are also recorded (just not via makePrincipalPayment()).
                if principal_pmt > 0:
                    tranche.makePrincipalPayment(principal_due, principal_pmt, period)
                else:
                    tranche.prinPmts[period] = 0
                    tranche.prinShortfalls[period] = principal_due
                    tranche.prinDue[period] = principal_due
                # subtract from available funds
                cash_amount -= principal_pmt

            # extra cash
            if cash_amount > 0:
                # add to cash reserves
                self._reserve_account = cash_amount

    def getWaterfall(self):
        '''
        Return list of lists containing Interest Due, Interest Paid, Interest Shortfall, Principal Paid, and Balance for
        each tranche for a given time period.
        '''
        return [[
            # interest due
            tranche.interestDue(tranche.period) + tranche.interestShortfalls[tranche.period - 1],
            # interest paid
            tranche.interestPmts[tranche.period],
            # interest shortfall
            tranche.interestShortfalls[tranche.period],
            # principal paid
            tranche.prinPmts[tranche.period],
            # balance
            tranche.notionalBalance(tranche.period)] for tranche in self._tranche_list]
