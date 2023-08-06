import math
from . import constants


def kaerber_ci(initial_dilution, dilution_step, replicates, exp_data, percentile=constants.PERC975):
    """
    Spearman-Kärber titration (CPD50) with confidence interval
    :param initial_dilution: initial dilution, e.g. 0.125
    :param dilution_step: dilution step, e.g. 0.5
    :param replicates: replicates or animals or etc.
    :param exp_data: list of experiment results, e.g. [0, 0, 1, 3, 3, 4, 4]
    :param percentile: percentile, e.g. 1.96 (for .975) by default
    :type initial_dilution: float
    :type dilution_step: float
    :type replicates: int
    :type exp_data: list
    :return: dict {lower: N, titer: N, upper: N} (all Ns are float)
    """
    # dilution d and all dilutions after have 100% cytopathic effect
    d = None
    for index, val in list(enumerate(reversed(exp_data))):
        if val != replicates:
            d = len(exp_data) - index
            break
    if d is None:
        return {'lower': None, 'titer': None, 'upper': None}

    log_d = math.log(initial_dilution) + math.log(dilution_step) * d
    positive_replicates = sum(exp_data[0:d + 1])
    log_titer = log_d - (math.log(dilution_step) * positive_replicates / replicates) + math.log(dilution_step)/2
    ci_numerator = sum(map(lambda x: x*(4-x), exp_data))
    standard_error = math.sqrt(math.log(dilution_step)**2 * ci_numerator/(replicates-1))
    return {'lower': math.exp(log_titer - standard_error),
            'titer': math.exp(log_titer),
            'upper': math.exp(log_titer + standard_error)}


def kaerber(initial_dilution, dilution_step, replicates, exp_data):
    """
    Spearman-Kärber titration (CPD50)
    :param initial_dilution: initial dilution, e.g. 0.125
    :param dilution_step: dilution step, e.g. 0.5
    :param replicates: replicates or animals or etc.
    :param exp_data: list of experiment results, e.g. [0, 0, 1, 3, 3, 4, 4]
    :type initial_dilution: float
    :type dilution_step: float
    :type replicates: int
    :type exp_data: list
    :return: titer (float)
    """
    return kaerber_ci(initial_dilution, dilution_step, replicates, exp_data)['titer']
