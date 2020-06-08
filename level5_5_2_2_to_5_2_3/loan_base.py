'''
Andy Zhang
2/16/2020
Case Study: Script for the Loan class
'''

from level5_5_2_2_to_5_2_3.asset import Asset  # using Asset class
import logging  # using logging module

'''=================================================
Loan class:
This module contains the Loan class.
================================================='''
class Loan(object):
    '''
    Class to model Loan object.

    Parameters
    ==========
    _asset : Asset object
        object of class Asset
    _term : int
        term of the loan (in months)
    _rate : float
        annual interest rate of loan
    _face : float / int
        principal of loan
    _defaulted : bool
        whether loan defaulted
    _defaultPeriod : int
        period where loan defaults
    _recoveryPercent : float
        percent of current assets value that can be recovered

    Methods
    =======
    __init__ method :
        initialize all object variables
    __str__ method :
        get str value of the Loan object
    @property assets :
        get Asset object
    @assets.setter assets :
        set Asset object
    @property term :
        get term of loan
    @term.setter term :
        set term of loan
    @property rate :
        get annual interest rate of loan
    @rate.setter rate :
        set annual interest rate of loan
    @property face :
        get principal of loan
    @face.setter face :
        set principal of loan
    @property defaultPeriod :
        get default period
    @property recoveryPercent :
        get percent of current assets value that can be recovered
    getRate :
        return annualized interest rate for a given period
    monthlyPayment :
        return the monthly loan payment, which is a combination of principal owed and interest charged
    totalPayments :
        return the sum of the principal and total interest charged
    totalInterest :
        return the total interest charged
    interestDueRecursive :
        wrap logs around interestDue_recursive() and then call it
    interestDue_recursive :
        return the interest charged for a particular period using recursion
    interestDue_formula :
        return the interest charged for a particular period using formula
    principalDueRecursive :
        wrap logs around principalDue_recursive() and then call it
    principalDue_recursive :
        return the principal due for a particular period using recursion
    principalDue :
        return the principal due for a particular period using formula
    balanceRecursive :
        wrap logs around balance_recursive() and then call it
    balance_recursive :
        return the current balance for a particular period using recursion
    balance_formula :
        return the current balance for a particular period using formula
    @classmethod calcMonthlyPmt :
        return the monthly loan payment, which is a combination of principal owed and interest charged
    @classmethod calcBalance :
        return the current balance for a particular period using formula
    balance :
        return the current balance for a particular period
    @staticmethod monthlyRate :
        return the monthly interest rate given the annual interest rate
    @staticmethod annualRate :
        return the annual interest rate given the monthly interest rate
    recoveryValue :
        return the amount of money that the lender can recover if the borrower defaults
    equity :
        return the available equity
    checkDefault :
        return whether the loan defaults or not in a particular period
    resetDefault :
        reset the loan to not defaulted
    '''

    # Case Study (previously 4.2.3 a)
    ###########

    def __init__(self, asset, term, rate, face, recovery_rate):
        '''
        Initialize variables.
        '''
        # initialization
        self._asset = None  # Asset object
        self._term = None  # term of loan (in months)
        self._rate = None  # annual interest rate
        self._face = None  # principal

        # Case Study
        ############

        self._defaulted = False  # loan hasn't defaulted
        self._defaultPeriod = None
        self._recoveryPercent = None  # recovery rate

        # check that inputs are valid
        # assets is not of type Asset
        if not isinstance(asset, Asset):
            logging.error(f'The assets input value given is {asset}' # in format, can use 'assets' since in the Asset 
                                                                     # class, __str__() method was recently added
                          f'. This is of type {type(asset)}, which is not valid in this case. The expected type for '
                          'assets is type Asset')
            raise TypeError('The assets should be of type Asset.')
        # term is not a positive int
        elif not (type(term) is int and term > 0):
            print('Term should be a positive integer.')
        # annual interest rate is not a nonnegative number
        ###############################################################################################################
        # Exercise 2.2.3 modification: For VariableMortgage, this would be None due to the design of the class, which #
        # would normally result in an error message. This condition is slightly modified to prevent that, and will be #
        # noted.                                                                                                      #
        ###############################################################################################################
        elif not (type(rate) is float and rate > 0 or rate is None):
            print('Annual interest rate should be a positive number. Note: Allowing None for VariableMortgage class.')
        # principal is not a nonnegative number
        elif not (type(face) is int and face >= 0 or type(face) is float and face >= 0):
            print('Principal should be a nonnegative number.')
        # recovery rate is not a nonnegative float
        elif not (type(recovery_rate) is float and recovery_rate >= 0):
            print('Recovery rate should be a nonnegative float.')
        # all inputs are valid
        else:
            self._asset = asset
            self._term = term
            self._rate = rate
            self._face = face
            self._defaultPeriod = self._term + 1
            self._recoveryPercent = recovery_rate

    # 4.3.7
    ##########

    def __str__(self):
        '''
        Return the str value of the Loan object.
        '''
        return f'Loan: assets value={self._asset.asset}, assets\'s annual depreciation rate=' \
               f'{self._asset.annualDeprRate()}, term={self._term}, rate={self._rate}, face={self._face}'

    # getters/setters

    # 2.2.7 a
    ###########

    @property
    def asset(self):
        '''
        Return the term of the loan.
        '''
        return self._asset

    # 4.2.3 a (previously 3.3.4)
    ###########

    @asset.setter
    def asset(self, iasset):
        '''
        Set the term of the loan.
        '''
        # iasset is not an Asset type
        if not isinstance(iasset, Asset):
            # error message
            logging.error(f'The iasset input value given is {iasset}. This is of type {type(iasset)}, which is not '
                          'valid in this case. The expected type for iasset is type Asset')
            raise TypeError('The assets should be of type Asset.')
        # iasset valid
        else:
            self._asset = iasset

    @property
    def term(self):
        '''
        Return the term of the loan.
        '''
        return self._term

    @term.setter
    def term(self, iterm):
        '''
        Set the term of the loan.
        '''
        # iterm is not positive integer
        if not (type(iterm) is int and iterm > 0):
            # error message
            print('The term must be a positive integer.')
        # iterm valid
        else:
            self._term = iterm

    @property
    def rate(self):
        '''
        Return the rate used in the loan.
        '''
        return self._rate

    @rate.setter
    def rate(self, irate):
        '''
        Set the rate used in the loan.
        '''
        # irate is a nonnegative number
        if not (type(irate) is float and irate > 0):
            # error message
            print('The annual interest rate must be a positive (float) number.')
        # irate valid
        else:
            self._rate = irate

    @property
    def face(self):
        '''
        Return the face value / principal of the loan.
        '''
        return self._face

    @face.setter
    def face(self, iface):
        '''
        Set the face value / principal of the loan.
        '''
        # iface is not nonnegative number
        if not (type(iface) is int and iface >= 0 or type(iface) is float and iface >= 0):
            # error message
            print('The principal must be a nonnegative number.')
        # iterm valid
        else:
            self._face = iface

    # Part 3.4
    ###########

    @property
    def defaultPeriod(self):
        '''
        Return the default period of the loan.
        '''
        return self._defaultPeriod

    @property
    def recoveryPercent(self):
        '''
        Return percent of current assets value that can be recovered.
        '''
        return self._recoveryPercent

    # 4.2.3 a (previously 2.2.1)
    ################

    def getRate(self, period):
        '''
        Overridden by derived classes, where its functionality is returning the annualized interest rate for the given
        period.
        '''
        # Should be overridden by derived classes.
        logging.error('The Loan class\'s getRate() method will be overridden by its derived class\'s getRate() method.')
        raise NotImplementedError()

    # Case Study (previously 4.2.3 b)
    ################

    def monthlyPayment(self, period):
        '''
        Return the monthly payment of the loan while accounting for period-dependent loan types.
        '''
        # period is not a nonnegative integer
        if not (type(period) is int and period >= 0):
            # error message
            print('The period must be a nonnegative integer.')
            return

        return self.calcMonthlyPmt(self._face, self.getRate(period), self._term)

    # Part 3.4 (previously 4.2.3 b)
    ################

    def totalPayments(self, period):
        '''
        Return the total payments of the loan while accounting for period-dependent monthly payments.
        '''
        # period is not a positive integer
        if not (type(period) is int and period > 0):
            # error message
            print('The period must be a positive integer.')
            return

        # monthly payment
        monthlyPmt = self.monthlyPayment(period)

        # total payment
        logging.debug('totalPayments() function calls the monthlyPayment() method to get the monthly payment of '
                      f'{monthlyPmt}, and multiplies this by the term of the loan to get the total payments.')
        return monthlyPmt * (self._defaultPeriod - 1)

    def totalInterest(self, period):
        '''
        Return the total interest of the loan while accounting for period-dependent monthly payments.
        '''
        # period is not a positive integer
        if not (type(period) is int and period > 0):
            # error message
            print('The period must be a positive integer.')
            return

        # total payments
        totalPmt = self.totalPayments(period)

        # total interest
        logging.debug('totalInterest() function calls the totalPayments() method to get the total payments of '
                      f'{totalPmt}, and subtracts the face value of the loan to get the total interest.')
        return totalPmt - self._face

    # Case Study (previously 4.2.3 b, c and e)
    ###################

    def interestDueRecursive(self, period):
        '''
        Wrap logs around interestDue_recursive() to avoid displaying recursive logs hundreds of times and then call it.
        '''
        # period is not a nonnegative integer
        if not (type(period) is int and period >= 0):
            # error message
            print('The period must be a nonnegative integer.')
            return

        # period is 0 or period is greater than or equal to defaultPeriod
        if period == 0 or period >= self._defaultPeriod:
            return 0
        # period is greater than the term
        elif period > self._term:
            logging.info(f'The period input is {period}. This is greater than the term of the loan, which is '
                         f'{self._term}, but should not be since interest should be all paid off by the end of the term'
                         ' of the loan. Period should be at most the term of the loan.')
            return self.interestDue_recursive(period)
        # period is greater than 0 but less than or equal to the term
        else:
            logging.warning('For even moderate periods, interestDue_recursive() function will be expected to take a long '
                         'time. It is strongly recommended to use interestDue_formula() function, which will be '
                         'significantly faster.')
            logging.debug('interestDue_recursive() function first calls the static-level method monthlyRate() to get '
                          'the monthly interest rate. It then calls balance_recursive() method to get the previous '
                          'period\'s balance via recursive calls to both balance_recursive() and '
                          'principalDue_recursive() methods, the latter of which uses monthlyPayment() method, which '
                          'uses the class-level method calcMonthlyPmt(). It finally takes the product of the monthly '
                          'interest rate and the previous balance to get the interest due.')
            return self.interestDue_recursive(period)

    def interestDue_recursive(self, period):
        '''
        Return the interest due in a given period using recursion.
        '''
        # period is greater than the term
        if period > self._term:
            return 0.
        # period is greater than 0 but less than or equal to the term
        else:
            if period >= self._defaultPeriod:
                return 0.
            return Loan.monthlyRate(self.getRate(period)) * self.balance_recursive(period - 1)

    # Case Study (previously 4.2.3 b and c)
    ###########

    def interestDue_formula(self, period):
        '''
        Return the interest due in a given period using formula.
        '''
        # period is not a nonnegative integer
        if not (type(period) is int and period >= 0):
            # error message
            print('The period must be a nonnegative integer.')
            return

        # period is 0 or period is greater than or equal to defaultPeriod
        if period == 0 or period >= self._defaultPeriod:
            return 0
        # period is greater than the term
        elif period > self._term:
            logging.info(f'The period input is {period}. This is greater than the term of the loan, which is '
                         f'{self._term}, but should not be since interest should be all paid off by the end of the term'
                         ' of the loan. Period should be at most the term of the loan.')
            return 0.
        # period is greater than 0 but less than or equal to the term
        else:
            # get monthly interest rate
            m_rate = Loan.monthlyRate(self.getRate(period))
            logging.debug('interestDue_formula() function first calls the static-level method monthlyRate() to get '
                          f'the monthly interest rate of {m_rate}.')

            # previous monthly payment
            monthlyPmt = self.monthlyPayment(period - 1)

            # interest due
            logging.debug('interestDue_formula() function finally uses the formula for interest due to calculate '
                          'interest due. The formula relies on monthlyPayment() method, which gives a monthly payment '
                          f'of {monthlyPmt}.')
            return m_rate * (self._face * (1 + m_rate)**(period - 1) - monthlyPmt *
                             ((1 + m_rate)**(period - 1) - 1) / m_rate)

    # Case Study (previously 4.2.3 b, c and e)
    ############

    def principalDueRecursive(self, period):
        '''
        Wrap logs around principalDue_recursive() to avoid displaying recursive logs hundreds of times and then call it.
        '''
        # period is not a nonnegative integer
        if not (type(period) is int and period >= 0):
            # error message
            print('The period must be a nonnegative integer.')
            return

        # period is 0 or period is greater than or equal to defaultPeriod
        if period == 0 or period >= self._defaultPeriod:
            return 0
        # period is greater than the term
        elif period > self._term:
            logging.info(f'The period input is {period}. This is greater than the term of the loan, which is '
                         f'{self._term}, but should not be since by the end of the term of the loan, the loan will be '
                         'fully paid off and so there won\'t be any principal left to pay. Period should be at most the'
                         ' term of the loan.')
            return self.principalDue_recursive(period)
        # period is greater than 0 but less than or equal to the term
        else:
            logging.warn('For even moderate periods, principalDue_recursive() function will be expected to take a long '
                         'time. It is strongly recommended to use principalDue() function, which will be significantly '
                         'faster.')
            logging.debug('principalDue_recursive() function calculates principal due as the product of monthly payment'
                          ' and interest due. Monthly payment is computed via monthlyPayment() method, which utilizes '
                          'the class-level method calcMonthlyPmt(), and interest due is computed via '
                          'interestDue_recursive() method, which calls both the static-level method monthlyRate() and '
                          'balance_recursive() method. balance_recursive() method gets the current period\'s balance '
                          'via recursive calls to both balance_recursive() and principalDue_recursive() methods, the '
                          'latter of which calls monthlyPayment() method that uses the class-level method '
                          'calcMonthlyPmt().')
            return self.principalDue_recursive(period)

    def principalDue_recursive(self, period):
        '''
        Return the principal due in a given period using recursion.
        '''
        # period is greater than the term
        if period > self._term:
            return 0.
        # period is greater than 0 but less than or equal to the term
        else:
            return self.monthlyPayment(period) - self.interestDue_recursive(period)

    # Case Study (previously 4.2.3 b and c)
    #############

    def principalDue(self, period):
        '''
        Return the principal due in a given period using formula.
        '''
        # period is not a nonnegative integer
        if not (type(period) is int and period >= 0):
            # error message
            print('The period must be a nonnegative integer.')
            return

        # period is 0 or period is greater than or equal to defaultPeriod
        if period == 0 or period >= self._defaultPeriod:
            return 0
        # period is greater than the term
        elif period > self._term:
            logging.info(f'The period input is {period}. This is greater than the term of the loan, which is '
                         f'{self._term}, but should not be since by the end of the term of the loan, the loan will be '
                         'fully paid off and so there won\'t be any principal left to pay. Period should be at most the'
                         ' term of the loan.')
            return 0.
        # period is greater than 0 but less than or equal to the term
        else:
            # get monthly interest rate
            m_rate = Loan.monthlyRate(self.getRate(period))
            logging.debug('principalDue() function first calls the static-level method monthlyRate() to get '
                          f'the monthly interest rate of {m_rate}.')

            # monthly payment
            monthlyPmtCurrent = self.monthlyPayment(period)
            monthlyPmtPrevious = self.monthlyPayment(period - 1)

            # principal due
            logging.debug('principalDue() function finally uses the formula for principal due to calculate principal '
                          'due. The formula relies on monthlyPayment() method, which gives a current monthly payment of'
                          f' {monthlyPmtCurrent} and a previous monthly payment of {monthlyPmtPrevious}')
            return monthlyPmtCurrent - m_rate * (self._face * (1 + m_rate)**(period - 1) -
                                                 monthlyPmtPrevious * ((1 + m_rate)**(period - 1) - 1) / m_rate)

    # Case Study (previously 4.2.3 b, c and e)
    #################

    def balanceRecursive(self, period):
        '''
        Wrap logs around balance_recursive() to avoid displaying recursive logs hundreds of times and then call it.
        '''
        # period is not a nonnegative integer
        if not (type(period) is int and period >= 0):
            # error message
            print('The period must be a nonnegative integer.')
            return

        # period is greater than or equal to defaultPeriod
        if period >= self._defaultPeriod:
            return 0
        # period is greater than the term
        elif period > self._term:
            logging.info(f'The period input is {period}. This is greater than the term of the loan, which is '
                         f'{self._term}, but should not be since by the end of the term of the loan, the loan will be '
                         'fully paid off and so there won\'t be any balance left. Period should be at most the term of '
                         'the loan.')
            return self.balance_recursive(period)
        # period is 0, or is greater than 0 but less than or equal to the term
        else:
            logging.warn('For even moderate periods, balance_recursive() function will be expected to take a long time.'
                         ' It is strongly recommended to use balance_formula() function, which will be significantly '
                         'faster.')
            logging.debug('balance_recursive() function calculates the balance as the difference between the previous '
                          'balance and current principal due. Previous balance and the current principal due are both '
                          'computed via recursive calls to principalDue_recursive(), balance_recursive(), and '
                          'interestDue_recursive() methods. principalDue_recursive() method utilizes monthlyPayment() '
                          'method, which then calls the class-level method calcMonthlyPmt(). interestDue_recursive() '
                          'method uses the static-level method monthlyRate().')
            return self.balance_recursive(period)

    def balance_recursive(self, period):
        '''
        Return the balance in a given period using recursion.
        '''
        # period 0
        if period == 0:
            # balance is simply principal
            return self._face
        # period is greater than the term
        elif period > self._term:
            return 0
        # period is greater than 0 but less than or equal to the term
        else:
            return self.balance_recursive(period - 1) - self.principalDue_recursive(period)

    # Case Study (previously 4.2.3 b and c)
    ############

    def balance_formula(self, period):
        '''
        Return the balance in a given period using formula.
        '''
        # period is not a nonnegative integer
        if not (type(period) is int and period >= 0):
            # error message
            print('The period must be a nonnegative integer.')
            return

        # period is greater than or equal to defaultPeriod
        if period >= self._defaultPeriod:
            return 0
        # period is 0
        elif period == 0:
            # balance is simply principal
            return self._face
        # period is greater than the term
        elif period > self._term:
            logging.info(f'The period input is {period}. This is greater than the term of the loan, which is '
                         f'{self._term}, but should not be since by the end of the term of the loan, the loan will be '
                         'fully paid off and so there won\'t be any balance left. Period should be at most the term of '
                         'the loan.')
            return 0
        # period is greater than 0 but less than or equal to the term
        else:
            # get monthly interest rate
            m_rate = Loan.monthlyRate(self.getRate(period))
            logging.debug('balance_formula() function first calls the static-level method monthlyRate() to get '
                          f'the monthly interest rate of {m_rate}.')

            # monthly payment
            monthlyPmt = self.monthlyPayment(period)

            # balance
            logging.debug('balance_formula() function finally uses the formula for balance to calculate balance. The '
                          f'formula relies on monthlyPayment() method, which gives a monthly payment of {monthlyPmt}.')
            return self._face * (1 + m_rate)**period - monthlyPmt * ((1 + m_rate)**period - 1) / m_rate

    # 4.2.3 b
    #############

    @classmethod
    def calcMonthlyPmt(cls, face, rate, term):
        '''
        Return the monthly payment given the face, rate and term of the loan.
        '''
        # check that inputs are valid
        # principal is not a nonnegative number
        if not (type(face) is int and face >= 0 or type(face) is float and face >= 0):
            print('Principal should be a nonnegative number.')
            return
        # annual interest rate is not a positive number
        elif not (type(rate) is float and rate > 0):
            print('Annual interest rate should be a positive number.')
            return
        # term is not a positive int
        elif not (type(term) is int and term > 0):
            print('Term should be a positive integer.')
            return

        # get monthly interest rate
        m_rate = Loan.monthlyRate(rate)
        # monthly payment
        return m_rate * face / (1 - (1 + m_rate) ** (-term))

    # Part 3.4
    ###########

    @classmethod
    def calcBalance(cls, face, rate, term, period):
        '''
        Return the balance for a given period given the face, rate and term of the loan.
        '''
        # check that inputs are valid
        # principal is not a nonnegative number
        if not (type(face) is int and face >= 0 or type(face) is float and face >= 0):
            print('Principal should be a nonnegative number.')
            return
        # annual interest rate is not a positive number
        elif not (type(rate) is float and rate > 0):
            print('Annual interest rate should be a positive number.')
            return
        # term is not a positive int
        elif not (type(term) is int and term > 0):
            print('Term should be a positive integer.')
            return
        # period is not a nonnegative integer
        elif not (type(period) is int and period >= 0):
            # error message
            print('The period must be a nonnegative integer.')
            return

        # period is greater than or equal to defaultPeriod
        if period >= Loan.defaultPeriod:
            return 0
        # period is 0
        elif period == 0:
            # balance is simply principal
            return face
        # period is greater than the term
        elif period > term:
            logging.info(f'The period input is {period}. This is greater than the term of the loan, which is {term}, but'
                         ' should not be since by the end of the term of the loan, the loan will be paid off and so '
                         'there won\'t be any balance left. Period should be at most the term of the loan.')
            return 0
        # period is greater than 0 but less than or equal to the term
        else:
            # get monthly interest rate
            m_rate = Loan.monthlyRate(rate)
            logging.debug('calcBalance() function first calls the static-level method monthlyRate() to get the monthly'
                          f' interest rate of {m_rate}.')

            # monthly payment
            monthlyPmt = cls.calcMonthlyPmt(face, rate, term)

            # balance
            logging.debug('calcBalance() function finally uses the formula for balance to calculate balance. The '
                          'formula relies on class-level method calcmonthlyPmt(), which gives a monthly payment of '
                          f'{monthlyPmt}.')
            return face * (1 + m_rate) ** period - monthlyPmt * ((1 + m_rate) ** period - 1) / m_rate

    # 4.2.3 b and c (previously 2.2.1)
    def balance(self, period):
        '''
        Return the balance for a given period.
        '''
        # period is not a nonnegative integer
        if not (type(period) is int and period >= 0):
            # error message
            print('The period must be a nonnegative integer.')
            return

        # period is greater than or equal to defaultPeriod
        if period >= self._defaultPeriod:
            return 0
        # period is 0
        elif period == 0:
            # balance is simply principal
            return self._face
        # period is greater than the term
        elif period > self._term:
            logging.info(f'The period input is {period}. This is greater than the term of the loan, which is '
                         f'{self._term}, but should not be since by the end of the term of the loan, the loan will be '
                         'paid off and so there won\'t be any balance left. Period should be at most the term of the '
                         'loan.')
            return 0
        # period is greater than 0 but less than or equal to the term
        else:
            # balance
            logging.debug('balance() function calls the class-level function calcBalance() to compute the current '
                          'balance of the loan.')
            return self.calcBalance(self._face, self.getRate(period), self._term, period)

    @staticmethod
    def monthlyRate(annual_rate):
        '''
        Return the monthly interest rate given an annual interest rate.
        '''
        # annual_rate is not a positive number
        if not (type(annual_rate) is float and annual_rate > 0):
            # error message
            print('The annual interest rate must be a positive number.')
            return
        return annual_rate / 12

    @staticmethod
    def annualRate(monthly_rate):
        '''
        Return the annual interest rate given a monthly interest rate.
        '''
        # monthly_rate is not a positive number
        if not (type(monthly_rate) is float and monthly_rate > 0):
            # error message
            print('The annual interest rate must be a positive number.')
            return
        return monthly_rate * 12

    # Case Study (previously 4.2.3 b and c)
    #############

    def recoveryValue(self, period):
        '''
        Return the recovery amount, i.e. the amount that can recovered if the borrower defaults, of the assets in its
        current state in given the period.
        '''
        # period is not a nonnegative integer
        if not (type(period) is int and period >= 0):
            # error message
            print('The period must be a nonnegative integer.')
            return

        # If period is greater than the term of the loan, then there is nothing for the lender to recover as the loan
        # has been completely paid off
        # period greater than loan's term
        if period > self.term:
            logging.info(f'The period input is {period}. This is greater than the term of the loan, which is '
                         f'{self._term}, but should not be since by the end of the term of the loan, the loan is '
                         'completely paid off and so there will be nothing to recover. Period should be at most the '
                         'term of the loan.')
            return 0.0
        # period is less than or equal to loan's term
        else:
            # recovery multiplier
            recovery_multiplier = self._recoveryPercent

            # current assets value
            currAssetValue = self._asset.currAssetVal(period)

            # recovery value
            logging.debug('recoveryValue() function computes the recovery value as the product of current assets value '
                          'and recovery multiplier. Current assets value is computed via the Asset class\'s '
                          f'currentAssetVal() method, which gives {currAssetValue}, and recovery multiplier is '
                          '{recovery_multiplier}.')
            return currAssetValue * recovery_multiplier

    # 4.2.3 b and c (previously 2.2.7 e)
    #############

    def equity(self, period):
        '''
        Return the available equity in the given the period.
        '''
        # period is not a nonnegative integer
        if not (type(period) is int and period >= 0):
            # error message
            print('The period must be a nonnegative integer.')
            return

        # loan balance
        loan_balance = self.balance(period)
        # If period is greater than the term of the loan, then the loan balance has been paid in full and so available
        # equity will simply be the current assets value.
        if period > self.term:
            logging.info(f'The period input is {period}. This is greater than the term of the loan, which is '
                         f'{self._term}, but should not be since by the end of the term of the loan, the loan balance '
                         'will be 0. Period should be at most the term of the loan.')
            loan_balance = 0.0

        # current assets value
        currAssetValue = self._asset.currAssetVal(period)

        # available equity
        logging.debug('equity() function computes equity as the difference between current assets value and current loan'
                      ' balance. Current assets value is computed via the Asset class\'s currentAssetVal() method, which'
                      f' gives {currAssetValue}, and current loan balance is computed via balance() method, which gives'
                      f' {loan_balance}.')
        return currAssetValue - loan_balance

    # Case Study
    ###################

    def checkDefault(self, period, num):
        '''
        Return whether or not the loan defaults in the given period.
        '''
        # not defaulted yet
        if not self._defaulted:
            # get whether loan defaulted
            self._defaulted = num == 0
            # Loan defaulted
            if self._defaulted:
                self._defaultPeriod = period  # get default period
                return self.recoveryValue(period)
            # Loan not defaulted
            return 0.
        # already defaulted
        else:
            return 0.

    def resetDefault(self):
        '''
        Reset the loan to not defaulted.
        '''
        self._defaulted = False
        self._defaultPeriod = self._term + 1
