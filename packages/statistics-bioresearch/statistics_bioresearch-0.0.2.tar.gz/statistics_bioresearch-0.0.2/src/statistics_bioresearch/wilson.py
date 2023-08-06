import math
from . import constants


def wilson_p(prevalence, sample_size, percentile):
    """
    :param prevalence: prevalence [0..1]
    :param sample_size: sample size (count of objects)
    :param percentile: percentile (default to PERC975)
    :type prevalence: float
    :type sample_size: int
    :type percentile: float
    :return: list of [lower, upper] borders of CI
    """
    a = percentile * percentile / (2 * sample_size)
    b = percentile * math.sqrt(
        (prevalence * (1 - prevalence)) / sample_size + percentile * percentile / (4 * sample_size * sample_size))
    c = 1 + percentile * percentile / sample_size
    return [(prevalence + a - b) / c, (prevalence + a + b) / c]


def wilson(positive, sample_size, percentile=constants.PERC975):
    """
    Wilson score interval
    :param positive: quantity of positive objects
    :param sample_size: sample size (count of objects)
    :param percentile: percentile (default to PERC975)
    :type positive: int
    :type sample_size: int
    :type percentile: float
    :return: list of [lower, upper] borders of CI
    """
    return wilson_p(positive / sample_size, sample_size, percentile)

