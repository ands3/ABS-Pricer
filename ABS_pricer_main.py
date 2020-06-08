'''
Andy Zhang
2/17/2020
Case Study: Test doWaterfall(); simulateWaterfall(); and runMonte(), with and without multiprocessing, methods (see
waterfall.py in waterfall folder).
'''

from level3_3_2_3.loan_pool import LoanPool  # using LoanPool class
from level5_5_2_2_to_5_2_3.house_base import HouseBase  # using HouseBase class
from level5_5_2_2_to_5_2_3.cars import Car  # using Car class
from level5_5_2_2_to_5_2_3.autoloan import AutoLoan  # using AutoLoan class
from liabilities.structured_securities import StructuredSecurities  # using StructuredSecurities class
from waterfall.waterfall import *  # import everything
import logging  # using logging module
import os  # using os module

'''=================================================
Main program (Python 2):
We test the doWaterfall(); simulateWaterfall(); and runMonte(), with and without multiprocessing, methods.
================================================='''
def main():
    logging.getLogger().setLevel(logging.WARN)

    print('\n=============== Part 1 ==============\n')

    # initialize lists for data
    loanIds = []  # loan number
    loanTypes = []  # loan type
    loanBalances = []  # loan balance
    loanRates = []  # loan rate
    loanTerms = []  # loan term
    assetNames = []  # assets name
    assetValues = []  # assets value

    # check if the provided csv file of loan data exists
    # csv file of loan data doesn't exist
    if not os.path.exists('Loans.csv'):
        print('The Loans.csv file doesn\'t exist.')
    # csv file of loan data exists
    else:
        # open csv file of loan data
        with open('Loans.csv', 'r') as f:
            # skip header
            next(f)
            # iterate through remaining lines
            for line in f:
                # extract relevant data
                loan_id, loan_type, loan_balance, loan_rate, loan_term, asset_name, asset_value = line.split(',')[:-4]
                # append data to appropriate lists
                loanIds.append(int(loan_id))  # convert loan ID to an integer and then append
                loanTypes.append(''.join(loan_type.split()))  # remove space, if any, from loan type and then append
                loanBalances.append(float(loan_balance))  # convert loan balance to a float and then append
                loanRates.append(float(loan_rate))  # covert loan rate to a float and then append
                loanTerms.append(int(loan_term))  # convert loan term to an integer and then append
                assetNames.append(asset_name)  # append asset name
                assetValues.append(float(asset_value))  # convert asset value to a float and then append

        # Create LoanPool object using the above loans
        loan_pool = LoanPool(
            # number of loans
            [0] * len(loanIds),
            # list of loan IDs
            loanIds,
            # list of Loan objects
            *[eval(loanType)(eval(assetName)(assetValue,
                                             # assuming Asset doesn't depreciate
                                             0.),
                             loanTerm, loanRate, loanBalance,
                             # assumed recovery rate for Asset
                             .35)
              for loanType, loanBalance, loanRate, loanTerm, assetName, assetValue
              in zip(loanTypes, loanBalances, loanRates, loanTerms, assetNames, assetValues)])

        # Create StructuredSecurities object with total notional from LoanPool object
        structured_securities = StructuredSecurities(loan_pool.totalLoanPrincipal(),
                                                     # assumed 'pro rata' here, but can also be 'sequential'; please
                                                     # consult "Elements of Structured Finance" by Ann Rutledge and
                                                     # Sylvain Raynes, pages 120-121 for more details.
                                                     'pro rata')
        # Add two standard tranches A and B
        structured_securities.addTranche(
            # derived Tranche class
            'StandardTranche',
            # tranche rate
            .05,
            # subordination level
            'A',
            # notional percent; note: .8 means 80% of notional
            .8,
            # relaxation coefficient; this is used in Part 3 for speeding up convergence when finding the implied
            # tranche rate
            .2)
        structured_securities.addTranche('StandardTranche', .08, 'B', .2, .8)

        print('---------------- Testing doWaterfall() function (write to csv part) ----------------\n')

        # call doWaterfall() to get payment values for each period on both assets and liabilities sides as well as each
        # tranche's IRR, DIRR, AL, and rating under the possibility of defaults in the loans
        # Note: the last two arguments, consideringDefaults and write_to_file, are set to False and True, respectively,
        # so that loan defaults are ignored and the resulting 'assets.csv' and 'liabilities.csv' can be written to file.
        # By default, as seen later, consideringDefaults=True and write_to_file=False.
        IRR_list, DIRR_list, AL_list, rating_list = doWaterfall(
            # LoanPool object
            loan_pool,
            # StructuredSecurities object
            structured_securities,
            # whether to consider defaults
            False,
            # whether to write to file
            True)

        # check that 'assets.csv' and 'liabilities.csv' both exist
        # 'asset.csv' and 'liabilities.csv' both exist
        if os.path.exists('assets.csv') and os.path.exists('liabilities.csv'):
            print('Both assets.csv and liabilities.csv have been created.')

        print('\n=============== Part 2 ==============\n')

        print('---------------- Testing doWaterfall() function (output metrics part) ----------------\n')

        # output each tranche's IRR, DIRR, AL, and rating
        for lvl, IRR, DIRR, AL, rating in zip(structured_securities.subordination_levels, IRR_list, DIRR_list, AL_list,
                                              rating_list):
            print(f'subordination level {lvl}: IRR = {IRR:.6f}, DIRR = {DIRR:.6f}, AL = {AL}; letter rating: {rating}')

        print('\n=============== Part 3 ==============\n')

        print('---------------- Testing simulateWaterfall() function ----------------\n')

        # Note: Commented out code below, if ran, takes a very long time!! Expect a few days. This global function is
        # used to aid the runMonte() global function below.

        # with Timer('time taken: ') as timer:
        #     # call simulateWaterfall() to get the average DIRR and WAL under the possibility of loan defaults for each
        #     # tranche via Monte Carlo simulation with 2000 simulations
        #     avgDIRR_list, WAL_list = simulateWaterfall(
        #         # LoanPool object
        #         loan_pool,
        #         # StructuredSecurities object
        #         structured_securities,
        #         # number of simulations
        #         2000)
        #
        #     # output each tranche's average DIRR and WAL
        #     for lvl, avgDIRR, WAL in zip(structured_securities.subordination_levels, avgDIRR_list, WAL_list):
        #         print(f'subordination level {lvl}: average DIRR = {avgDIRR:.6f}, WAL = {WAL:.6f}')

        print('\n---------------- Testing runMonte() function ----------------\n')

        # Note: Commented out code below, if ran, takes a very long time!! Expect a little more than a week (the version
        # below, which uses multiprocessing, took about 10 hours so this would take about 20 times more--200 hours or
        # almost 9 days). Please run the global function below this global function. That function is the same, except
        # it uses multiprocessing to speed things up. In particular, based on a past test, it should take about 10
        # hours.

        # # call runMonte() to find the implied tranche rates and thus the implied average DIRR, WAL, and yield
        # # (tranche rate)
        # avg_DIRR_list, WAL_list, yield_list = runMonte(
        #     # LoanPool object
        #     loan_pool,
        #     # StructuredSecurities object
        #     structured_securities,
        #     # tolerance
        #     .005,
        #     # number of simulations
        #     2000)
        # rating_list = [letterRating(avgDIRR) for avgDIRR in avg_DIRR_list]
        #
        # # output each tranche's implied average DIRR, WAL, and tranche rate
        # for lvl, avgDIRR, rating, WAL, y in zip(structured_securities.subordination_levels, avg_DIRR_list, rating_list,
        #                                         WAL_list, yield_list):
        #     print(f'subordination level {lvl}: average DIRR = {avgDIRR:.6f}, rating = {rating}, WAL = {WAL:.6f}, ' \
        #           f'rate = {y:.6f}')

        print('\n---------------- Testing runMonte(), now with multiprocessing ----------------\n')

        # call runMonte_multiprocessing() to find the implied tranche rates and thus the implied average DIRR, WAL, and
        # yield (tranche rate) via multiprocessing
        # Note: from a previous run, this should take about 10 hours.
        avg_DIRR_list, WAL_list, yield_list = runMonte_multiprocessing(
            # LoanPool object
            loan_pool,
            # StructuredSecurities
            structured_securities,
            # tolerance
            .005,
            # number of simulations
            2000,
            # number of processes to use for multiprocessing
            20)
        rating_list = [letterRating(avgDIRR) for avgDIRR in avg_DIRR_list]

        # output each tranche's implied average DIRR, WAL, and tranche rate
        for lvl, avgDIRR, rating, WAL, y in zip(structured_securities.subordination_levels, avg_DIRR_list, rating_list,
                                                WAL_list, yield_list):
            print(f'subordination level {lvl}: average DIRR = {avgDIRR:.6f}, rating = {rating}, WAL = {WAL:.6f}, ' \
                  f'rate = {y:.6f}')

if __name__=='__main__':
    main()
