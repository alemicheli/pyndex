import _decorator as dec
import pandas as pd


@dec.typeassert(array_indexes = list)
def join(array_indexes):
    return pd.concat(array_indexes, axis = 0).fillna(0)
    