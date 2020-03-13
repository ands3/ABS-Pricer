'''
Andy Zhang
1/20/2020
Exercises 4.2.3 - 4.2.4: Script for classes related to Mortgages.
'''

from loans import VariableRateLoan, FixedRateLoan  # using derived classes of Loan class

'''=================================================
MortgageMixin, VariableMortgage, and FixedMortgage classes:
This module contains the MortgageMixin, VariableMortgage, and FixedMortgage classes.
================================================='''

# 2.2.2
class MortgageMixin(object):
    '''
    Mixin class for mortgages.

    Methods
    =======
    __init__ method :
        initialize all object variables
    PMI :
        return PMI
    monthlyPayment :
        return the monthly loan payment, which is a combination of principal owed, interest charged, and PMI
    principalDue :
        return the principal due for a particular period
    '''

    # 2.2.7 b
    ##############

    def __init__(self, home, term, rate, face):
        '''
        Initialize variables.
        '''
        # call super to ensure that __init__ of derived classes of Loan class gets called after
        super(MortgageMixin, self).__init__(home, term, rate, face)

    # 4.2.3 b
    ################

    def PMI(self, period):
        '''
        Return the PMI in a given period.
        '''
        # period is not a nonnegative integer
        if not (type(period) is int and period >= 0):
            # error message
            print 'The period must be a nonnegative integer.'
            return

        # loan-to-value (LTV) ratio
        # cf. https://www.kitces.com/blog/eliminating-private-mortgage-insurance-pmi-principal-preayment-downpayment-80-ltv/
        LTV = FixedRateLoan.calcBalance(self._asset.asset, self._rate, self._term, period) / self._asset.asset

        # PMI paid whenever LTV >= 80%
        # assuming loan face value equals home value
        logging.debug('PMI() function computes PMI as 0.0075% of the loan face value, which is assumed to be the '
                      'initial assets value, if LTV is at least 0.8. LTV is computed via the base class\'s class-level '
                      'method calcMonthlyPmt(), which gives {LTV}.'.format(LTV=LTV))
        return .000075 * self._asset.asset if LTV >= .8 else 0.0

    def monthlyPayment(self, period):
        '''
        Return the monthly payment of the loan while accounting for period-dependent loan types.
        '''
        # Get monthly payment from base class.
        monthlyPmt = super(MortgageMixin, self).monthlyPayment(period)

        # Not affected by PMI; clarified by Mark in email
        return monthlyPmt

    # 4.2.3 b
    ################

    def principalDue(self, period):
        '''
        Return the principal due in a given period using formula.
        '''
        # Get principal due from base class.
        principal_due = super(MortgageMixin, self).principalDue(period)

        # PMI
        pmi = self.PMI(period)

        # principal due is None
        if not principal_due:
            return
        # principal due is not None
        # Affected by PMI: reduced by PMI; clarified by Mark in email
        logging.debug('principalDue() function computes principal due as the difference between principal due and PMI. '
                      'Principal due is computed via the base class\'s principalDue() method, which gives '
                      '{principal_due}, and PMI is computed via PMI() method, which gives {PMI}.'.
                      format(principal_due=principal_due, PMI=pmi))
        return principal_due - self.PMI(period)

# 2.2.3
##########

class VariableMortgage(MortgageMixin, VariableRateLoan):
    '''
    Class to model VariableMortgage object.
    '''
    pass

class FixedMortgage(MortgageMixin, FixedRateLoan):
    '''
    Class to model FixedMortgage object.
    '''
    pass
