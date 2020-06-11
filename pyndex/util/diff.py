import pyndex.util._decorator as dec
import pandas as pd

@dec.typeassert(before = pd.core.frame.DataFrame,
                 after = pd.core.frame.DataFrame)
def diff(before,after):
    active_before = before[(before > 0)].dropna(axis=1).columns
    active_after = after[(after > 0)].dropna(axis=1).columns
    deletions = active_before.drop(
                active_before.intersection(active_after)).to_frame(index=False)
    additions = active_after.drop(
                active_after.intersection(active_before)).to_frame(index=False)
    return additions, deletions
