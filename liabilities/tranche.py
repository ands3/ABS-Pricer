'''
Andy Zhang
2/17/2020
Case Study: Script for the Tranche class
'''

import numpy_financial as npf  # using numpy-financial module
import operator  # using operator module
import logging  # using logging module
from functools import reduce  # using selective importing

'''=================================================
Tranche class:
This module contains the Tranche class.
================================================='''
class Tranche(object):
    '''
    Class to model Tranche object.

    Parameters
    ==========
    _notional : float / int
        notional of tranche
    _rate : float
        annual interest rate
    _subordination : str
        subordination level of tranche

    Methods
    =======
    __init__ method :
        initialize all object variables
    @property notional :
        get the notional of tranche
    @notional.setter notional :
        set the notional of tranche
    @property rate :
        get annual interest rate
    @rate.setter rate :
        set annual interest rate
    @property subordination :
        get subordination level of tranche
    @subordination.setter subordination :
        set subordination level of tranche
    getNotional :
        return the notional of tranche
    @classmethod IRR:
        return the annualized internal rate of return (IRR)
    @classmethod DIRR:
        return the reduction in yield (DIRR)
    @classmethod AL:
        return the average life (AL)
    '''

    def __init__(self, notional: float or int, rate: float, subordination: str):
        '''
        Initialize variables.
        '''
        # initialization
        self._notional = None  # notional
        self._rate = None  # annual interest rate
        self._subordination = None  # subordination level

        # check that inputs are valid
        # notional is not a nonnegative number
        if not (type(notional) is int and notional >= 0 or type(notional) is float and notional >= 0):
            raise ValueError('Notional should be a nonnegative number.')
        # rate is not a positive number
        if not (type(rate) is float and rate > 0):
            raise ValueError('Annual interest rate should be a positive number.')
        # subordination level is not a string
        if type(subordination) is not str:
            raise TypeError('Subordination level should be a string.')
        # all inputs are valid
        else:
            self._notional = notional
            self._rate = rate
            self._subordination = subordination

    # getters/setters

    @property
    def notional(self) -> float or int:
        '''
        Return the notional of tranche.
        '''
        return self._notional

    @notional.setter
    def notional(self, inotional: float):
        '''
        Set the notional of tranche.
        '''
        # check if inotional is a nonnegative number
        # inotional is not a nonnegative number
        if not (type(inotional) is int and inotional >= 0 or type(inotional) is float and inotional >= 0):
            raise ValueError('inotional should be a nonnegative number.')
        # inotional valid
        else:
            self._notional = inotional

    @property
    def rate(self) -> float:
        '''
        Return annual interest rate.
        '''
        return self._rate

    @rate.setter
    def rate(self, irate: float):
        '''
        Set annual interest rate.
        '''
        # check if irate is a positive number
        # irate is not a positive number
        if not (type(irate) is float and irate > 0):
            raise ValueError('irate should be a positive number.')
        # irate valid
        else:
            self._rate = irate

    @property
    def subordination(self) -> str:
        '''
        Return the subordination level of tranche.
        '''
        return self._subordination

    @subordination.setter
    def subordination(self, isubordination: str):
        '''
        Set the subordination level of tranche.
        '''
        # check if isubordination is a str
        # isubordination is not a str
        if type(isubordination) is not str:
            raise ValueError('isubordination should be a str.')
        # isubordination valid
        else:
            self._subordination = isubordination

    def getNotional(self):
        '''
        Overridden by derived classes, where its functionality is returning the notional of tranche.
        '''
        # Should be overridden by derived classes.
        raise NotImplementedError()

    # Part 2.4
    #############

    @classmethod
    def IRR(cls, notional: float or int, totalPmts: float) -> float:
        '''
        Return the annualized internal rate of return (IRR).
        '''
        logging.debug(f'IRR() class method takes the tranche notional of {notional} and all periodic payments, both '
                      f'interest and principal, made to the tranche of {totalPmts} and uses those to compute IRR via '
                      'npf.irr(). The resulting number is then annualized to get the annualized Internal Rate of '
                      'Return.')
        return npf.irr([-notional] + totalPmts) * 12

    # Part 2.5
    #############

    @classmethod
    def DIRR(cls, rate: float, notional: float or int, totalPmts: float) -> float:
        '''
        Return the reduction in yield (DIRR).
        '''
        IRR = cls.IRR(notional, totalPmts)
        logging.debug(f'DIRR() class method takes the IRR computed via the class method IRR() of {IRR} and subtracts '
                      f'that from the tranche rate of {rate} to get the Reduction in Yield.')
        # Note: Since npf.irr() is a numerical technique, sometimes it returns an IRR that is higher than rate. This
        # results in a negative DIRR. When calculating yield, this poses some problems as WAL is positive and so
        # applying sqrt() results in complex numbers. To remedy this issue, max() is applied.
        return max(rate - IRR, 0.0)

    # Part 2.6
    #############

    @classmethod
    def AL(cls, prinPmts: dict[int, float], notional: float or int, balance: float or int) -> None or float:
        '''
        Return the average life (AL).
        '''
        # loan paid down
        if balance == 0:
            logging.debug('Assuming that the loan was paid down, i.e., balance goes down to 0, AL() class method '
                          'computes the Average Life by first taking the dot product of all principal payments and '
                          'their respective periods and then dividing by the tranche notional.')
            # cf. https://stackoverflow.com/questions/4093989/dot-product-in-python
            return reduce(operator.add, map(operator.mul, prinPmts.keys(), prinPmts.values())) / notional

