'''
Andy Zhang
1/6/2020
Exercise 2.2.6 b: Script for derived Car class.
'''

# using Asset class
from level5_5_2_2_to_5_2_3.asset import Asset

'''=================================================
Car class:
This module contains the Car class.
================================================='''
# 2.2.1 a
class Car(Asset):
    '''
    Class to model Car object.

    Methods
    =======
    annualDeprRate :
        return yearly depreciation rate
    '''

    def annualDeprRate(self) -> float:
        '''
        Return the annual depreciation rate.
        '''
        # Overrides the base Asset class

        # annual depreciation rate
        return self._depr_rate
