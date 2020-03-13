'''
Andy Zhang
1/20/2020
Exercises 4.2.3 - 4.2.4: Script for the Asset class
'''

# using logging module
import logging

'''=================================================
Asset class:
This module contains the Asset class.
================================================='''
class Asset(object):
    '''
    Class to model Asset object.

    Parameters
    ==========
    _asset : float / int
        initial assets value
    _depr_rate : float
        yearly depreciation rate

    Methods
    =======
    __init__ method :
        initializes all object variables
    __str__ method :
        get str value of the Asset object
    @property assets :
        get initial assets value
    @assets.setter assets :
        set initial assets value
    annualDeprRate :
        return yearly depreciation rate
    @staticmethod monthlyDeprRate :
        return monthly depreciation rate
    currAssetVal :
        return current assets value
    '''

    def __init__(self, asset, depr_rate):
        '''
        Initialize variables.
        '''
        # initialization
        self._asset = None  # assets value
        self._depr_rate = None  # yearly depreciation rate

        # check that inputs are valid
        # assets value is not a positive number
        if not (type(asset) is int and asset > 0 or type(asset) is float and asset > 0):
            print 'Asset value should be a positive number.'
        # annual depreciation rate is not a nonnegative number
        elif not (type(depr_rate) is float and depr_rate >= 0):
            print 'Annual depreciation rate should be a nonnegative number.'
        # all inputs are valid
        else:
            # 2.1.6 a
            self._asset = asset
            self._depr_rate = depr_rate

    # 4.2.3 a
    ############

    def __str__(self):
        '''
        Return the str value of the Asset object.
        '''
        return 'Asset: assets={asset}, depr_rate={depr}'.format(asset=self._asset, depr=self._depr_rate)

    # getters/setters

    @property
    def asset(self):
        '''
        Return the initial assets value.
        '''
        return self._asset

    @asset.setter
    def asset(self, iasset):
        '''
        Set the initial assets value.
        '''
        # iasset is not positive integer
        if not (type(iasset) is int and iasset > 0 or type(iasset) is float and iasset > 0):
            # error message
            print 'Asset value must be a positive number.'
        # iasset valid
        else:
            self._asset = iasset

    # 4.2.3 a (previously 2.2.6 a)
    def annualDeprRate(self):
        '''
        Overridden by derived classes, where its functionality is returning the annual depreciation rate.
        '''

        # Should be overridden by derived classes.
        logging.error('The Asset class\'s annualDeprRate() method will be overridden by its derived class\'s '
                      'annualDeprRate() method.')
        raise NotImplementedError()

    # Part 3.4 (previously 2.1.6 c)
    #############

    @staticmethod
    def monthlyDeprRate(ann_depr_rate):
        '''
        Return the monthly depreciation rate given the annual depreciation rate.
        '''
        # ann_depr_rate is a nonnegative number
        if not (type(ann_depr_rate) is float and ann_depr_rate >= 0):
            # error message
            print 'Yearly depreciation rate must be a nonnegative number.'
            return
        return ann_depr_rate / 12

    # 2.1.6 d
    def currAssetVal(self, t):
        '''
        Return the value of the assets at period t, accounting for depreciation.
        '''
        # period is not a nonnegative integer
        if not (type(t) is int and t >= 0):
            # error message
            print 'The period must be a nonnegative integer.'
            return

        # get monthly depreciation rate
        m_rate = Asset.monthlyDeprRate(self._depr_rate)

        # total depreciation
        total_depr = (1. - m_rate)**t

        # current assets value
        return self._asset * total_depr
