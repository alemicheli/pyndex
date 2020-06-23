import pyndex.util._decorator as dec
import pandas as pd
import warnings


def _single_slice_warning(before, after):
    before_len = len(before.index)
    after_len = len(after.index)
    if (before_len != 1):
        warnings.warn(f'''First argument DataFrame has {before_len}
                        rows, different from 1.
                        Function supported with 1 row.
                        ''')
    if (after_len != 1):
        warnings.warn(f'''Second argument DataFrame has {after_len}
                        rows, different from 1.
                        Function supported with 1 row.
                        ''')


@dec.typeassert(before=pd.DataFrame,
                after=pd.DataFrame)
def diff(before, after):
    """Find difference in constituents between two indexes.

    Args:
        before (pandas.DataFrame): First Index
        after (pandas.DataFrame): Second Index

    Returns:
        pandas.DataFrame: Two pandas DataFrame containing additions
        and deletions.

    Example:
    >>> db = wrds.Connection()
    >>> index_1 = pyndex.Index.from_wrds(db, 2010, "3000")["2010-06-30":"2010-06-30"]
    >>> index_2 = pyndex.Index.from_wrds(db, 2011, "3000")["2011-06-30":"2011-06-30"]
    >>> additions, deletions = pyndex.diff(index_1, index_2)

    Intended to find additions and deletions between two events/dates.
    """
    _single_slice_warning(before, after)
    active_before = before[(before > 0)].dropna(axis=1).columns
    active_after = after[(after > 0)].dropna(axis=1).columns
    deletions = active_before.drop(
        active_before.intersection(active_after)).to_frame(index=False)
    additions = active_after.drop(
        active_after.intersection(active_before)).to_frame(index=False)
    return additions, deletions
