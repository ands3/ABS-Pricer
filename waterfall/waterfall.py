'''
Andy Zhang
2/17/2020
Case Study: Script for doWaterfall(), simulateWaterfall(), runMonte(), runMonte_multiprocessing(), and
runSimulationParallel() functions.
'''

from level3_3_2_3.loan_pool import LoanPool  # using LoanPool class
from liabilities.structured_securities import StructuredSecurities  # using StructuredSecurities class
from liabilities.tranche import Tranche  # using Tranche class
from level5_5_2_2_to_5_2_3.timer import Timer  # using Timer decorator
from math import sqrt, exp  # selective importing
from operator import is_not  # using is_not() operator
from functools import partial  # using partial() method
import multiprocessing  # using multiprocessing module
import time  # using time module
import logging  # using logging module

'''=================================================
letterRating function:
We write a function that takes Reduction in Yield (DIRR) as input and returns the corresponding letter rating.
================================================='''
def letterRating(DIRR):
    '''
    Take Reduction in Yield (DIRR) and output the corresponding letter rating.

    Parameters
    ==========
    DIRR : float
        Reduction in Yield (DIRR)

    Returns
    =======
    return value : str
        corresponding letter rating

    Examples
    ========
    letterRating(.0006) -> Aaa
    letterRating('gh') -> ValueError
    '''
    # check that DIRR input is valid
    # DIRR is not a number
    if not (type(DIRR) is float):
        raise TypeError('DIRR should be a number.')
    # DIRR is valid
    else:
        # dict of ABS ratings
        ABSrating = {.06: 'Aaa', .67: 'Aa1', 1.3: 'Aa2', 2.7: 'Aa3', 5.2: 'A1', 8.9: 'A2', 13: 'A3', 19: 'Baa1',
                     27: 'Baa2', 46: 'Baa3', 72: 'Ba1', 106: 'Ba2', 143: 'Ba3', 183: 'B1', 231: 'B2', 311: 'B3',
                     2500: 'Caa', 10000: 'Ca'}
        # Loop through through keys.
        for k in sorted(ABSrating.keys()):
            # Find first key that DIRR is less than or equal to
            if DIRR * 10000 <= k:
                return ABSrating[k]

'''=================================================
doWaterfall function:
We write a function that takes a LoanPool object and a StructuredSecurities object as well as whether to consider 
defaults (consideringDefaults) and whether to write to file (write_to_file) and keeps getting periodic payments from the 
LoanPool object to pay the StructuredSecurities object until there are no more active loans in the LoanPool object. It 
then outputs the periodic results for the LoanPool object into assets.csv and the periodic results for the 
StructuredSecurities object into liabilities.csv. Finally, it computes and returns for each tranche, the waterfall 
metrics: Internal Rate of Return (IRR), Reduction in Yield (DIRR), Average Life (AL) and letter rating and outputs them.
================================================='''
def doWaterfall(loan_pool, structured_securities, consideringDefaults=True, write_to_file=False):
    '''
    Keep getting periodic payments from the LoanPool object to pay the StructuredSecurities object until there are no
    more active loans in the LoanPool object, and then output the periodic results for the LoanPool object into
    assets.csv and the periodic results for the StructuredSecurities object into liabilities.csv. In addition, the
    waterfall metrics, Internal Rate of Return (IRR), Reduction in Yield (DIRR), Average Life (AL), and letter rating,
    for each tranche are computed and returned.

    Parameters
    ==========
    loan_pool : LoanPool object
        LoanPool object
    structured_securities : StructuredSecurities object
        StructuredSecurities object
    consideringDefaults : bool
        whether to consider loan defaults
    write_to_file : bool
        whether to write the results to file

    Returns
    =======
    IRR_list : list of float
        list of tranche's Internal Rate of Return (IRR)
    DIRR_list : list of float
        list of tranche's Reduction in Yield (DIRR)
    AL_list : list of float
        list of tranche's Average Life (AL)
    rating_list : list of str
        list of tranche ratings
    '''
    # check if inputs are valid
    # loan_pool is not of type LoanPool
    if not isinstance(loan_pool, LoanPool):
        logging.error('The inputted loan_pool is of type {type}, which is not a LoanPool object. A LoanPool object '
                      'should be inputted instead.'.format(type=type(loan_pool)))
        raise TypeError('loan_pool is not a LoanPool object, but it should be.')
    # structured_securities is not of type StructuredSecurities
    elif not (isinstance(structured_securities, StructuredSecurities)):
        logging.error('The inputted structured_securities is of type {type}, which is not a StructuredSecurities '
                      'object. A StructuredSecurities object should be inputted instead.'.
                      format(type=type(structured_securities)))
        raise TypeError('structured_securities is not a StructuredSecurities object, but it should be.')
    # write_to_file is not bool
    elif not isinstance(write_to_file, bool):
        raise TypeError('write_to_file should be a bool.')
    # all inputs are valid
    else:
        # reset each loan's default period back to original state
        for ln in loan_pool:
            ln.resetDefault()
        # reset iterator's index back to 0
        loan_pool.reset_index()
        # reset each tranche back to state at time 0
        for tranche in structured_securities:
            tranche.reset()
        # reset iterator's index back to 0
        structured_securities.reset_index()

        period = 0

        f_assets = None
        f_liabilities = None
        if write_to_file:
            # open assets.csv file to write to
            f_assets = open('assets.csv', 'w')
            f_assets_headers = ['Period'] + ['{ID} Principal Due,{ID} Interest Due,{ID} Balance'.format(ID=ID)
                                             for ID in sorted(loan_pool.loan_ids)]
            f_assets.write(','.join(f_assets_headers))

            # open liabilities.csv file to write to
            f_liabilities = open('liabilities.csv', 'w')
            f_liabilities_headers = ['Period'] + ['{lvl} Interest Due,{lvl} Interest Paid,{lvl} Interest Shortfall,' \
                                                  '{lvl} Principal Paid,{lvl} Balance'.format(lvl=level)
                                                  for level in sorted(structured_securities.subordination_levels)]
            f_liabilities.write(','.join(f_liabilities_headers) + ',Cash (Reserve)')

        logging.debug('doWaterfall() function takes the payments received from LoanPool via its aggTotalPmtDue() and '
                      'checkDefaults() methods as cash available and uses them to pay StructuredSecurities via '
                      'makePayments() method. It first pays off all interest payments to the tranches via '
                      'makeInterestPayment() method and then principal payments via makePrincipalPayment() method. '
                      'After all payments are made, any reserve cash is added to the next period\'s cash available.')
        # loop while there are payments coming from loan pool
        while loan_pool.aggTotalPmtDue(period) > 0 or period == 0:
            recoveries = 0.
            if consideringDefaults:
                # any recoveries from defaults
                recoveries = loan_pool.checkDefaults(period) if period > 0 else 0.0

            # loan_pool's total payment in current time period
            total_pmt = loan_pool.aggTotalPmtDue(period) + recoveries

            # pay total payment to StructuredSecurities
            structured_securities.makePayments(total_pmt, loan_pool, recoveries)

            # get waterfall on both LoanPool and StructuredSecurities
            loan_pool_waterfall = loan_pool.getWaterfall(period)
            structuredSecurities_waterfall = structured_securities.getWaterfall()

            # reserve account balance
            reserve = structured_securities.reserve_account

            if write_to_file:
                # save loan pool's waterfall to assets.csv
                assets_line = '\n' + ','.join([str(period)] + [str(round(value, 2))
                                                               for ln in loan_pool_waterfall for value in ln])
                f_assets.write(assets_line)

                # save structured securities' waterfall to liabilities.csv
                liabs_line = '\n' + \
                             ','.join([str(period)] + [str(round(value, 2)) for tranche in structuredSecurities_waterfall
                                                       for value in tranche] + [str(round(reserve, 2))])
                f_liabilities.write(liabs_line)

            # increase time period
            period += 1
            structured_securities.increaseTimePeriodOfTranches()

        if write_to_file:
            # close files
            f_assets.close()
            f_liabilities.close()

        IRR_list = []  # list of tranche's IRR
        DIRR_list = []  # list of tranche's DIRR
        AL_list = []  # list of tranche's AL
        rating_list = []  # list of tranche's letter rating
        # compute waterfall metrics
        for tranche in structured_securities:
            # periods in chronological order
            periods = sorted(tranche.prinPmts.keys())[1:]

            # total payments in chronological order
            totalPayments = [tranche.prinPmts[period] + tranche.interestPmts[period] for period in periods]

            # IRR
            IRR = Tranche.IRR(tranche.notional, totalPayments)

            # DIRR
            DIRR = Tranche.DIRR(tranche.rate, tranche.notional, totalPayments)
            # letter rating
            rating = letterRating(DIRR)

            # AL
            AL = Tranche.AL(tranche.prinPmts, tranche.notional, tranche.notionalBalance(periods[-1]))

            # append IRR, DIRR, AL, and letter rating
            IRR_list.append(IRR)
            DIRR_list.append(DIRR)
            AL_list.append(AL)
            rating_list.append(rating)

        # reset iterator's index back to 0
        structured_securities.reset_index()

        return IRR_list, DIRR_list, AL_list, rating_list

'''=================================================
simulateWaterfall function:
We write a function that takes a LoanPool object, a StructuredSecurities object, and the number of simulations (NSIM) to
run and calls doWaterfall() function NSIM times, each time recording each tranches' DIRR and AL under possible default 
as an entry within the lists of DIRR and AL. It then averages the DIRR and AL values of each tranche and returns these 
values as lists, where each entry in the DIRR and AL lists pertains to a tranche.
================================================='''
def simulateWaterfall(loan_pool, structured_securities, NSIM):
    '''
    Take as inputs a LoanPool object, a StructuredSecurities object, and the number of simulations (NSIM) to run, call
    doWaterfall() function NSIM times, averages the DIRR and AL values obtained for each tranche, and return these
    values as lists, where each entry in the DIRR and AL lists pertains to a tranche.

    Parameters
    ==========
    loan_pool : LoanPool object
        LoanPool object
    structured_securities : StructuredSecurities object
        StructuredSecurities object
    NSIM : int
        number of simulations

    Returns
    =======
    avg_DIRR_list :
        list of each tranche's average DIRR from NSIM simulations
    WAL_list :
        list of each tranche's WAL from NSIM simulations
    '''
    # check if all inputs are valid
    # loan_pool is not of type LoanPool
    if not isinstance(loan_pool, LoanPool):
        logging.error('The inputted loan_pool is of type {type}, which is not a LoanPool object. A LoanPool object '
                      'should be inputted instead.'.format(type=type(loan_pool)))
        raise TypeError('loan_pool is not of type LoanPool.')
    # structured_securities is not of type StructuredSecurities
    elif not isinstance(structured_securities, StructuredSecurities):
        logging.error('The inputted structured_securities is of type {type}, which is not a StructuredSecurities '
                      'object. A StructuredSecurities object should be inputted instead.'.
                      format(type=type(structured_securities)))
        raise TypeError('structured_securities is not of type StructuredSecurities.')
    # NSIM is not a positive integer
    elif not (type(NSIM) is int and NSIM > 0):
        raise ValueError('NSIM should be a positive integer.')
    # all inputs are valid
    else:
        # initialize lists for DIRR and AL
        DIRR_list = []
        AL_list = []
        # run NSIM simulations
        for _ in xrange(NSIM):
            # get DIRR and AL
            # Note: the last two arguments, consideringDefaults and write_to_file, are missing as we are assuming their
            # default values, namely, consideringDefaults=True and write_to_file=False
            _, DIRR, AL, _ = doWaterfall(loan_pool, structured_securities)
            DIRR_list.append(DIRR)
            AL_list.append(AL)

        # cf. https://stackoverflow.com/questions/19261747/sum-of-n-lists-element-wise-python
        # average DIRR
        avg_DIRR_list = [sum(DIRR) / NSIM for DIRR in zip(*DIRR_list)]
        # WAL
        # cf. https://stackoverflow.com/questions/16096754/remove-none-value-from-a-list-without-removing-the-0-value
        WAL_list = [sum(filter(partial(is_not, None), AL)) / NSIM for AL in zip(*AL_list)]

        return avg_DIRR_list, WAL_list

'''=================================================
calculateYield function:
We write a function that takes the WAL and average DIRR as inputs and computes and returns the corresponding yield.
================================================='''
def calculateYield(WAL, DIRR):
    '''
    Return the yield associated with a given WAL and average DIRR.

    Parameters
    ==========
    WAL : float
        average AL
    DIRR : float
        average DIRR

    Returns
    =======
    return value : float
        yield

    Examples
    ========
    calculateYield(.1, .9) -> 0.0649869562545
    calculateYield(.1, '.9') -> ValueError
    calculateYield('.1', .9) -> ValueError
    '''
    # check that inputs are valid
    # WAL is not a nonnegative number
    if not (type(WAL) is float and WAL >= 0 or type(WAL) is int and WAL >= 0):
        raise ValueError('WAL should be a nonnegative number.')
    # DIRR is not a nonnegative number
    elif not (type(DIRR) is float and DIRR >= 0 or type(DIRR) is int and DIRR >= 0):
        raise ValueError('DIRR should be a nonnegative number.')
    # all inputs valid
    else:
        return (7 / (1 + .08 * exp(-.19 * WAL / 12)) + .019 * sqrt(WAL / 12. * DIRR * 100)) / 100

'''=================================================
runMonte function:
We write a function that takes a LoanPool object, a StructuredSecurities object, tolerance, and the number of 
simulations (NSIM) as inputs. It then enters an infinite loop where 1) simulateWaterfall() function is called to get 
each tranche's WAL and average DIRR, 2) these values are used to compute each tranche's yield and consequently each 
tranche's new rate, and 3) the differences between each tranche's old and new rates are computed and compared against 
the tolerance level to determine if there is convergence. Upon convergence, lists of each tranche's average DIRR, WAL, 
and yield are returned.
================================================='''
@Timer('time taken: ')
def runMonte(loan_pool, structured_securities, tolerance, NSIM):
    '''
    Take a LoanPool object, a StructuredSecurities object, tolerance, and the number of simulations (NSIM) as inputs and
    then enter an infinite loop where simulateWaterfall() function is called to get each tranche's WAL and average DIRR,
    these values are used to compute each tranche's yield and consequently each tranche's new rate, and the differences
    between each tranche's old and new rates are computed and compared against the tolerance level to determine if there
    is convergence. Upon convergence, return lists of each tranche's average DIRR, WAL, and yield.

    Parameters
    ==========
    loan_pool : LoanPool object
        LoanPool object
    structured_securities : StructuredSecurities object
        StructuredSecurities object
    tolerance : float
        tolerance level for difference in tranches' old and new rates
    NSIM : int
        number of simulations

    Returns
    =======
    avg_DIRR_list : list of float
        list of each tranche's average DIRR
    WAL_list : list of float
        list of each tranche's WAL
    yields : list of float
        list of each tranche's yield
    '''
    # check if all inputs are valid
    # loan_pool is not of type LoanPool
    if not isinstance(loan_pool, LoanPool):
        logging.error('The inputted loan_pool is of type {type}, which is not a LoanPool object. A LoanPool object '
                      'should be inputted instead.'.format(type=type(loan_pool)))
        raise TypeError('loan_pool is not of type LoanPool.')
    # structured_securities is not of type StructuredSecurities
    elif not isinstance(structured_securities, StructuredSecurities):
        logging.error('The inputted structured_securities is of type {type}, which is not a StructuredSecurities '
                      'object. A StructuredSecurities object should be inputted instead.'.
                      format(type=type(structured_securities)))
        raise TypeError('structured_securities is not of type StructuredSecurities.')
    # tolerance is not a positive float
    elif not (type(tolerance) is float and tolerance > 0):
        raise ValueError('tolerance is not a positive number.')
    # NSIM is not a positive integer
    elif not (type(NSIM) is int and NSIM > 0):
        raise ValueError('NSIM should be a positive integer.')
    # all inputs are valid
    else:
        while True:
            # get average DIRR and WAL for tranches
            avg_DIRR_list, WAL_list = simulateWaterfall(loan_pool, structured_securities, NSIM)

            diff_num = 0.0  # for diff formula
            yields = []  # list of each tranche's yield
            # iterate through each tranche to compute the numerator of the 'diff' formula
            for DIRR, WAL, tranche, relaxation_coef in zip(avg_DIRR_list, WAL_list, structured_securities,
                                                           structured_securities.relaxation_coefs):
                # get yield
                y = calculateYield(WAL, DIRR)

                # get new tranche rate
                oldRate = tranche.rate
                newRate = oldRate + relaxation_coef * (y - oldRate)

                diff_num += tranche.notional * abs((oldRate - newRate) / oldRate)

                # set tranche rate to new rate
                tranche.rate = newRate
                yields.append(newRate)

            # reset iterator's index back to 0
            structured_securities.reset_index()

            # get difference between old and new tranche rates
            diff = diff_num / structured_securities.total_notional

            # check if diff is lower than or equal to tolerance
            # diff is lower than or equal to tolerance
            if diff <= tolerance:
                return avg_DIRR_list, WAL_list, yields

'''=================================================
runMonte_multiprocessing function:
We write a function that takes a LoanPool object, a StructuredSecurities object, tolerance, the number of simulations
(NSIM) and the number of processes (numProcesses) as inputs. It then enters an infinite loop where 1)
simulateWaterfall() function is called to get each tranche's WAL and average DIRR using multiprocessing, 2) these values
are used to compute each tranche's yield and consequently each tranche's new rate, and 3) the differences between each
tranche's old and new rates are computed and compared against the tolerance level to determine if there is convergence.
Upon convergence, lists of each tranche's average DIRR, WAL, and yield are returned.
================================================='''
@Timer('total runtime: ')
def runMonte_multiprocessing(loan_pool, structured_securities, tolerance, NSIM, numProcesses):
    '''
    Take a LoanPool object, a StructuredSecurities object, tolerance, the number of simulations (NSIM), and the number
    of processes (numProcesses) as inputs and then enter an infinite loop where simulateWaterfall() function is called
    to get each tranche's WAL and average DIRR using multiprocessing, these values are used to compute each tranche's
    yield and consequently each tranche's new rate, and the differences between each tranche's old and new rates are
    computed and compared against the tolerance level to determine if there is convergence. Upon convergence, return
    lists of each tranche's average DIRR, WAL, and yield.

    Parameters
    ==========
    loan_pool : LoanPool object
        LoanPool object
    structured_securities : StructuredSecurities object
        StructuredSecurities object
    tolerance : float
        tolerance level for difference in tranches' old and new rates
    NSIM : int
        number of simulations
    numProcesses : int
        number of processes to use for multiprocessing

    Returns
    =======
    avg_DIRR_list : list of float
        list of each tranche's average DIRR
    WAL_list : list of float
        list of each tranche's WAL
    yields : list of float
        list of each tranche's yield
    '''
    # check if all inputs are valid
    # loan_pool is not of type LoanPool
    if not isinstance(loan_pool, LoanPool):
        logging.error('The inputted loan_pool is of type {type}, which is not a LoanPool object. A LoanPool object '
                      'should be inputted instead.'.format(type=type(loan_pool)))
        raise TypeError('loan_pool is not of type LoanPool.')
    # structured_securities is not of type StructuredSecurities
    elif not isinstance(structured_securities, StructuredSecurities):
        logging.error('The inputted structured_securities is of type {type}, which is not a StructuredSecurities '
                      'object. A StructuredSecurities object should be inputted instead.'.
                      format(type=type(structured_securities)))
        raise TypeError('structured_securities is not of type StructuredSecurities.')
    # tolerance is not a positive float
    elif not (type(tolerance) is float and tolerance > 0):
        raise ValueError('tolerance is not a positive number.')
    # NSIM is not a positive integer
    elif not (type(NSIM) is int and NSIM > 0):
        raise ValueError('NSIM should be a positive integer.')
    # numProcesses is not a positive integer and it is a divisor that results in no remainder
    elif not (type(numProcesses) is int and numProcesses > 0 and NSIM % numProcesses == 0):
        raise ValueError('numProcesses should be a positive integer.')
    # all inputs are valid
    else:
        while True:
            # get average DIRR and WAL for tranches for each process
            avg_DIRR_list, WAL_list = runSimulationParallel(loan_pool, structured_securities, NSIM, numProcesses)

            diff_num = 0.0  # for diff formula
            yields = []  # list of each tranche's yield
            # iterate through each tranche to compute the numerator of the 'diff' formula
            for DIRR, WAL, tranche, relaxation_coef in zip(avg_DIRR_list, WAL_list, structured_securities,
                                                           structured_securities.relaxation_coefs):
                # get yield
                y = calculateYield(WAL, DIRR)

                # get new tranche rate
                oldRate = tranche.rate
                newRate = oldRate + relaxation_coef * (y - oldRate)

                diff_num += tranche.notional * abs((oldRate - newRate) / oldRate)

                # set tranche rate to new rate
                tranche.rate = newRate
                yields.append(newRate)

            # reset iterator's index back to 0
            structured_securities.reset_index()

            # get difference between old and new tranche rates
            diff = diff_num / structured_securities.total_notional

            # check if diff is lower than or equal to tolerance
            # diff is lower than or equal to tolerance
            if diff <= tolerance:
                return avg_DIRR_list, WAL_list, yields

'''=================================================
doWork function:
We write a function that takes the input and output queues to be used for multiprocessing and uses the input queue
values to fill the output queue.
================================================='''
def doWork(input_, output):
    '''
    Fill the output queue using the input queue.
    '''
    f, args = input_.get(timeout=1)
    res = f(*args)
    output.put(res)

'''=================================================
getTrancheMetrics function:
We create a function that gets the results of the processes used and then averages them to get each tranche's average
DIRR and WAL.
================================================='''
def getTrancheMetrics(input_queue, output_queue):
    '''
    Keep getting results from the output queue until the number of results matches the length of the input queue and
    then average the results to get each tranche's average DIRR and WAL.
    '''
    avgDIRR_results = []
    WAL_results = []
    # keep getting from output queue until length of results list equals length of input queue
    while len(avgDIRR_results) < input_queue.qsize():
        # get result from output queue
        r = output_queue.get()

        # add to average DIRR results and WAL results lists
        avgDIRR_results.append(r[0])
        WAL_results.append(r[1])

    # average values in average DIRR results and WAL results lists element-wise to get each tranche's average DIRR and
    # WAL
    return [sum(avgDIRR) / len(avgDIRR_results) for avgDIRR in zip(*avgDIRR_results)], \
           [sum(WAL) / len(WAL_results) for WAL in zip(*WAL_results)]

'''=================================================
runSimulationParallel function:
We create a function that takes a LoanPool object, a StructuredSecurities object, the number of simulations (NSIM) and
the number of processes (numProcesses), utilizes numProcesses processes to each compute the tranche metrics and averages
these results, and then returns each tranche's metrics.
================================================='''
def runSimulationParallel(loan_pool, structured_securities, NSIM, numProcesses):
    '''
    Take a LoanPool object, a StructuredSecurities object, the number of simulations (NSIM) and the number of processes
    (numProcesses), utilize numProcesses processes to each compute the tranche metrics, average these results, and then
    return each tranche's metrics.

    Parameters
    ==========
    loan_pool : LoanPool object
        LoanPool object
    structured_securities : StructuredSecurities object
        StructuredSecurities object
    NSIM : int
        number of simulations
    numProcesses : int
        number of processes to use for multiprocessing

    Returns
    =======
    avg_DIRR_list : list of float
        list of each tranche's average DIRR
    WAL_list : list of float
        list of each tranche's WAL
    '''
    # check if inputs are all valid
    # loan_pool is not of type LoanPool
    if not isinstance(loan_pool, LoanPool):
        logging.error('The inputted loan_pool is of type {type}, which is not a LoanPool object. A LoanPool object '
                      'should be inputted instead.'.format(type=type(loan_pool)))
        raise TypeError('loan_pool is not of type LoanPool.')
    # structured_securities is not of type StructuredSecurities
    elif not isinstance(structured_securities, StructuredSecurities):
        logging.error('The inputted structured_securities is of type {type}, which is not a StructuredSecurities '
                      'object. A StructuredSecurities object should be inputted instead.'.
                      format(type=type(structured_securities)))
        raise TypeError('structured_securities is not of type StructuredSecurities.')
    # NSIM is not a positive integer
    elif not (type(NSIM) is int and NSIM > 0):
        raise ValueError('NSIM should be a positive integer.')
    # numProcesses is not a positive integer nor a factor of NSIM
    elif not (type(numProcesses) is int and numProcesses > 0 and NSIM % numProcesses == 0):
        raise ValueError('numProcesses should be a positive integer that is a factor of NSIM.')
    # all inputs are valid
    else:
        # initialize queues
        input_queue = multiprocessing.Queue()
        output_queue = multiprocessing.Queue()

        # give each process the same number of simulations
        for i in range(numProcesses):
            input_queue.put((simulateWaterfall, (loan_pool, structured_securities, NSIM / numProcesses,)))

        # create and initialize numProcesses processes
        procs = []
        for _ in range(numProcesses):
            proc = multiprocessing.Process(target=doWork, args=(input_queue, output_queue))
            procs.append(proc)
            proc.start()

        # get each tranche's average DIRR and WAL
        avgDIRR, WAL = getTrancheMetrics(input_queue, output_queue)

        # terminate all processes
        for proc in procs:
            proc.terminate()

        # Note: sleep() is used to ensure that all processes are finished and terminated before returning values.
        # Otherwise, there can potentially be empty values. 10 is chosen here to ensure that all 2000 simulations get
        # completed. It may not be the optimal number if more than 2000 simulations are used.
        time.sleep(numProcesses * 10)

        return avgDIRR, WAL
