import pyndex.util._decorator as dec
import pandas as pd


@dec.typeassert(array_indexes=list)
def join(array_indexes):
    """Join list of Russell Indexes of type pandas.DataFrame.

    Args:
        array_indexes (list): List of Indexes

    Returns:
        pandas.core.DataFrame: Joined indexes.

    Example:
    >>> db = wrds.Connection()
    >>> index_1 = px.Index.from_wrds(db, 2010, "3000")
    >>> index_2 = px.Index.from_wrds(db, 2010, "3000")
    >>> joined_index = px.join([index_1,index_2])

    Can join any index, but mostly intended for joining indexes of consecutive
    years.
    """
    return pd.concat(array_indexes, axis=0).fillna(0)
