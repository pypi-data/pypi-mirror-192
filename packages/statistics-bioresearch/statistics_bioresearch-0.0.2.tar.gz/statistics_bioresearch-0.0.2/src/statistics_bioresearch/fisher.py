import math
from . import constants


def phi(prevalence):
    """
    :param prevalence: prevalence [0..1]
    :type prevalence: float
    """
    return 2 * (math.asin(prevalence ** 0.5))


def sphi(sample_size):
    """
    :param sample_size: sample size
    :type sample_size: int
    """
    return 1 / (sample_size ** 0.5)


def fisher_p(prevalence, sample_size, percentile):
    """
    :param prevalence: prevalence [0..1]
    :param sample_size: sample size (count of objects)
    :param percentile: percentile (default to PERC975)
    :type prevalence: float
    :type sample_size: int
    :type percentile: float
    :return: list of [lower, upper] borders of CI
    """
    return [
        math.sin((phi(prevalence) - percentile * sphi(sample_size)) / 2) ** 2,  # lower border of CI
        math.sin((phi(prevalence) + percentile * sphi(sample_size)) / 2) ** 2   # upper border of CI
    ]


def fisher(positive, sample_size, percentile=constants.PERC975):
    """
    :param positive: quantity of positive objects
    :param sample_size: sample size (count of objects)
    :param percentile: percentile (default to PERC975)
    :type positive: int
    :type sample_size: int
    :type percentile: float
    :return: list of [lower, upper] borders of CI
    """
    return fisher_p(positive / sample_size, sample_size, percentile)

