'''
Andy Zhang
1/6/2020
Exercise 2.2.7: Script for fixed AutoLoan class, a derived FixedRateLoan class.
'''

from loans import FixedRateLoan  # using a derived class of Loan class

'''=================================================
AutoLoan class:
This module contains the fixed AutoLoan class.
================================================='''

# 2.2.4

# Since AutoLoans don't require PMI, AutoLoan class simply derives from the FixedRateLoan class;
# cf. https://www.mortgagecalculator.org/calcs/car.php
class AutoLoan(FixedRateLoan):
    '''
    Class to model AutoLoan object.

    Methods
    =======
    __init__ method :
        initialize all object variables
    '''

    # 2.2.7 c
    ##############

    def __init__(self, car, term, rate, face, recovery_rate):
        '''
        Initialize variables.
        '''
        # call super to ensure that __init__ of derived classes of Loan class gets called after
        super(FixedRateLoan, self).__init__(car, term, rate, face, recovery_rate)
