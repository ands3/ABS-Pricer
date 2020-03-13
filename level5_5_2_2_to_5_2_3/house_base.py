'''
Andy Zhang
1/6/2020
Exercise 2.2.6 c: Script for derived HouseBase class.
'''

# using Asset class
from asset import Asset

'''=================================================
HouseBase class:
This module contains the HouseBase class.
================================================='''
# 2.2.1 a
class HouseBase(Asset):
    '''
    Class to model House object.

    Methods
    =======
    annualDeprRate :
        return yearly depreciation rate
    '''

    def annualDeprRate(self):
        '''
        Return the annual depreciation rate.
        '''
        # Overrides the base Asset class

        # annual depreciation rate
        return self._depr_rate
