import warnings

DEFAULT_EPSILON_PARAMETER = 0.0001
DEFAULT_NUMBER_OF_POINTS = 1000

id2key = {
    27: 'esc',
    -1: 'sleep'
}

def epsilon_validator(value):
    if value > DEFAULT_EPSILON_PARAMETER:
        warnings.warn(
            f'Epsilon value is too high.' \
            f'Please, set epsilon value smaller than {DEFAULT_EPSILON_PARAMETER}.'
        )
        warnings.warn(
            f'Fallback to default epsilon value {DEFAULT_EPSILON_PARAMETER}'
        )

        return DEFAULT_EPSILON_PARAMETER
    else:
        try:
            1/value
        except:
            raise TypeError(
                f'Epsilon value should be float. Got {value}'
            )


def number_of_points_validator(value):
    if value < DEFAULT_NUMBER_OF_POINTS:
        warnings.warn(
            f'Number of points too low.' \
            f'Please, set number of points greater than {DEFAULT_NUMBER_OF_POINTS}'
        )
        warnings.warn(
            f'Fallback to default numbre of points {DEFAULT_NUMBER_OF_POINTS}'
        )

        return DEFAULT_NUMBER_OF_POINTS

    if not isinstance(value, int):
        raise TypeError(
            f'Number of points should be int. Got {value}'
        )

    return value