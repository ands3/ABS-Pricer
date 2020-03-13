'''
Andy Zhang
1/7/2020
Stripped-down version from Exercises 1.5.7 - 1.5.8 for the purposes of Exercise 3.1.2 c that uses the reduce function
'''

'''=================================================
sumproduct function:
We write a function that takes a number and a tuple of two numbers, adds the first number to the product of the numbers 
in the tuple, and returns the resulting sum
================================================='''
def sumproduct(total, (num1, num2)):
    '''
    Output the result of total + num1*num2

    Parameters
    ==========
    total : int/float
        a number
    num1 : int/float
        first number in pair
    num2 : int/float
        second number in pair

    Returns
    =======
    return value : float
        total + num1*num2

    Examples
    ========
    sumproduct('a', (5, 6)) -> None
    sumproduct(1.0, (2, 4.5)) -> 10.0
    '''

    # inputs are all numbers
    if type(total) is int or type(total) is float or type(num1) is int or type(num1) is float or type(num2) is int \
            or type(num2) is float:
        return total + num1*num2

'''=================================================
WeightedAverageMaturity function:
We write a function that takes a list of mortgage tuples (amount, rate, term) and outputs the Weighted Average Maturity 
using the reduce function and a regular function, sumproduct, as its callable
================================================='''
def WeightedAverageMaturity(mortgage_terms):
    '''
    Output the Weighted Average Maturity (term)

    Parameters
    ==========
    mortgage_terms : list of tuple of (int/float, float, int)
        list of tuple of (amount, rate, term)

    Returns
    =======
    wam : float
        weighted average maturity (term) of mortgages

    Examples
    ========
    WeightedAverageMaturity([()]) -> None
    WeightedAverageMaturity([(100000, .025, 10)]) -> 10
    WeightedAverageMaturity([(130000, .027, 12), (900000, .055, 120), (550000, .044, 50)]) -> 86.746835443
    '''

    # check that input is valid
    # input is not a list of at least one mortgage term
    if type(mortgage_terms) is not list or len(mortgage_terms) == 0:
        print 'The list of mortgage terms needs to have at least one mortgage term.'
        return
    # list doesn't consist of tuples of 3 elements
    elif any(type(term) is not tuple or len(term) != 3 for term in mortgage_terms):
        print 'Each mortgage terms in the list of mortgage terms needs to be a tuple of (face, rate, term).'
        return
    # tuples aren't of type (int/float, float, int)
    elif any(not (type(amount) is int or type(amount) is float) or type(rate) is not float or type(term) is not int
             for amount, rate, term in mortgage_terms):
        print 'Each mortgage term (face, rate, term) in the list of mortgage terms needs to be of (int/float, float, ' \
              'int).'
        return

    # get mortgage amounts and terms
    amounts, _, terms = zip(*mortgage_terms)

    # compute weighted average maturity

    # total mortgage amount
    total_mortgage = sum(amounts)

    # Weighted Average Maturity
    wam = reduce(sumproduct, zip(amounts, terms), 0.0) / total_mortgage

    return wam

'''=================================================
WeightedAverageRate function:
We write a function that takes a list of mortgage tuples (amount, rate, term) and outputs the Weighted Average Rate 
using the reduce function with lambda callable
================================================='''
def WeightedAverageRate(mortgage_terms):
    '''
    Output the Weighted Average Rate

    Parameters
    ==========
    mortgage_terms : list of tuple of (int/float, float, int)
        list of tuple of (amount, rate, term)

    Returns
    =======
    war : float
        weighted average rate of mortgages

    Examples
    ========
    WeightedAverageRate([()]) -> None
    WeightedAverageRate([(100000, .025, 10)]) -> 0.025
    WeightedAverageRate([(130000, .027, 12), (900000, .055, 120), (550000, .044, 50)]) -> 0.0488670886076
    '''

    # check that input is valid
    # input is not a list of at least one mortgage term
    if type(mortgage_terms) is not list or len(mortgage_terms) == 0:
        print 'The list of mortgage terms needs to contain at least one mortgage term.'
        return
    # list doesn't consist of tuples of 3 elements
    elif any(type(term) is not tuple or len(term) != 3 for term in mortgage_terms):
        print 'Each mortgage terms in the list of mortgage terms needs to be a tuple of (face, rate, term).'
        return
    # tuples aren't of type (int/float, float, int)
    elif any(not (type(amount) is int or type(amount) is float) or type(rate) is not float or type(term) is not int
             for amount, rate, term in mortgage_terms):
        print 'Each mortgage term (face, rate, term) in the list of mortgage terms needs to be of (int/float, float, ' \
              'int).'
        return

    # get mortgage amounts and rates
    amounts, rates, _ = zip(*mortgage_terms)

    # compute weighted average rate

    # total mortgage amount
    total_mortgage = sum(amounts)

    # Weighted Average Rate
    war = reduce(lambda total, (amount, rate): total + amount*rate, zip(amounts, rates), 0.0) / total_mortgage

    return war