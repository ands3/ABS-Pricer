'''
Andy Zhang
1/25/2020
Exercise 4.2.2: Script for the Timer class
'''

from time import time  # selective importing to use time() function
import logging  # use logging module
from functools import wraps  # use wraps() method

# set logging level to info
logging.getLogger().setLevel(logging.INFO)

'''=================================================
Timer class:
This module contains the Timer class.
================================================='''
class Timer(object):
    '''
    Class to model Timer object.

    Parameters
    ==========
    warnThreshold : float
        class-level threshold
    _start_time : float
        start time
    _units : str
        units for time
    _conv_factor : float
        factor to convert from seconds to minutes / hours
    _name : str
        name of Timer class instance

    Methods
    =======
    __init__ method :
        initializes all object variables
    __enter__ method :
        enter the context manager and start timer
    __exit__ method :
        exit the context manager and stop timer
    __call__ method :
        allows Timer class to work as a decorator
    configureTimerDisplay :
        change timer units
    '''

    # 4.2.2 a
    #############

    # units in seconds
    warnThreshold = 60.

    def __init__(self, name: str):
        '''
        Initialize variables.
        '''
        # initialize
        self._start_time = None  # start time
        self._units = 'secs'  # timer's unit of time measure; default is always in seconds
        self._conv_factor = 1.  # conversion factor for different units of time
        self._name = None

        # check name input is str
        # name input is invalid
        if type(name) is not str:
            raise TypeError('Name input should be str.')
        # valid name input
        else:
            self._name = name

    def __enter__(self):
        '''
        Enter the context manager and start the timer.
        '''
        # start timer
        self._start_time = time()
        # set these to the variable after 'as' in 'with ... as ...'
        return self

    # 4.2.2 b (previously 4.2.1)
    ##############

    def __exit__(self, *args):
        '''
        Exit the context manager and stop the timer. Time taken displayed using warn-level log statement if it exceeds
        threshold.
        '''

        # time taken (in secs)
        time_taken = time() - self._start_time

        # check if threshold exceeded
        # threshold exceeded
        if time_taken > Timer.warnThreshold:
            # warn-level log when warnThreshold exceeded
            logging.warning(f'{self._name}: {(time() - self._start_time) * self._conv_factor} {self._units}')
        # threshold not exceeded
        else:
            # info-level log when warnThreshold not exceeded
            logging.info(f'{self._name}: {(time() - self._start_time) * self._conv_factor} {self._units}')

    # 5.2.1
    #############

    # cf. https://stackoverflow.com/questions/9213600/function-acting-as-both-decorator-and-context-manager-in-python
    def __call__(self, f):
        '''
        Allows Timer class to work as a decorator.
        '''
        @wraps(f)
        def wrapped(*args, **kwargs):
            '''
            Wrap Timer class around function f.
            '''
            s = self.__enter__()
            res = f(*args, **kwargs)
            e = time()
            print(f'{f}: {e-s._start_time} seconds')
            return res
        return wrapped

    def configureTimerDisplay(self, new_units: str):
        '''
        Set the unit of measurement for the timer. Default is seconds. Can set to minutes or hours.
        '''
        # check if new timer units is a valid one
        # if not valid, print error message
        if new_units not in ['secs', 'mins', 'hrs']:
            logging.info(f'The input value is \'{new_units}\'. It\'s not one of the three possible options. Valid inputs'
                         ' are: \'secs\' (seconds), \'mins\' (minutes), or \'hrs\' (hours). The current units of '
                         f'{self._units} will be used.')
        # valid, so change timer units to new units
        else:
            # change units
            self._units = new_units
            # change conversion factor; base unit is always in seconds by default
            # new units is in minutes
            if new_units == 'mins':
                self._conv_factor = 1/60.
            # new units is in hours
            elif new_units == 'hrs':
                self._conv_factor = 1/60.**2
