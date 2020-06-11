import pyndex.util._decorator as dec
import pandas as pd


@dec.typeassert(before=pd.core.frame.DataFrame,
                after=pd.core.frame.DataFrame)
def diff(before, after):
    """Find difference in constituents between two indexes.

    Args:
        before (pandas.core.DataFrame): First Index 
        after (pandas.core.DataFrame): Second Index 

    Returns:
        pandas.core.DataFrame: Two pandas DataFrame containing additions
        and deletions.

    Example:
    >>> db = wrds.Connection()
    >>> index_1 = pyndex.Index.from_wrds(db, 2010, "3000")["2010-06-30":"2010-06-30"]
    >>> index_2 = pyndex.Index.from_wrds(db, 2011, "3000")["2011-06-30":"2011-06-30"]
    >>> additions, deletions = pyndex.diff(index_1, index_2)

    Intended to find additions and deletions between two events/dates.
    """
    active_before = before[(before > 0)].dropna(axis=1).columns
    active_after = after[(after > 0)].dropna(axis=1).columns
    deletions = active_before.drop(
        active_before.intersection(active_after)).to_frame(index=False)
    additions = active_after.drop(
        active_after.intersection(active_before)).to_frame(index=False)
    return additions, deletions
