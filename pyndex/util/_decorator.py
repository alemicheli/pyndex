from inspect import signature
from functools import wraps
import calendar
from pandas.tseries.offsets import BDay
from workalendar.usa import NewYork

cal = NewYork()


def typeassert(*ty_args, **ty_kwargs):
    def decorate(func):

        # Mapfunction argument names to supplied types
        sig = signature(func)
        bound_types = sig.bind_partial(*ty_args, **ty_kwargs).arguments

        @wraps(func)
        def wrapper(*args, **kwargs):
            bound_values = sig.bind(*args, **kwargs)
            # Enforce type assertions across supplied arguments
            for name, value in bound_values.arguments.items():
                if name in bound_types:
                    if not isinstance(value, bound_types[name]):
                        raise TypeError(
                            'Argument {} must be {}'.format(
                                name, bound_types[name])
                        )
            return func(*args, **kwargs)

        return wrapper
    return decorate


def validatebday(rank_day=True):
    def decorate(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            result_day = func(*args, **kwargs)

            while not cal.is_working_day(result_day):
                if rank_day:
                    result_day -= BDay(1)
                else:
                    result_day += BDay(1)
                result_day = result_day.date()
            return result_day

        return wrapper

    return decorate


def supported(*supp_args, **supp_kwargs):
    def decorate(func):
        # Map function argument names to supplied types
        sig = signature(func)
        supported_val = sig.bind_partial(*supp_args, **supp_kwargs).arguments

        @wraps(func)
        def wrapper(*args, **kwargs):
            bound_values = sig.bind(*args, **kwargs)
            # Enforce type assertions across supplied arguments
            for name, value in bound_values.arguments.items():
                if name in supported_val:
                    if not (value in supported_val[name]):
                        raise ValueError(
                            'Argument {} must be among {}'.format(
                                name, supported_val[name])
                        )
            return func(*args, **kwargs)

        return wrapper
    return decorate
