import pyndex.util._decorator as dec
import pyndex.core.algorithm as alg
import wrds
import pandas as pd


class Index:

    @staticmethod
    @dec.typeassert(wrds=wrds.sql.Connection,
                    year=int, index=str)
    @dec.supported(index=["1000", "2000", "3000"])
    def from_wrds(wrds, year, index, verbose=False):
        """Generate Russell Indexes from WRDS database.

        Args:
            wrds (wrds.sql.Connection): Connection to the WRDS database.
            year (int): Year of the Index to be reconstructed.
            index (str): Index to reconstructed. Supported Russell 1000, 2000 and 3000.
            verbose (bool, optional): Verbose output. Defaults to False.

        Returns:
            pandas.core.DataFrame: DataFrame MultiIndex 

        Examples:
        Construct an Russell 3000 Index from year 2010.
        >>> db = wrds.Connection()
        >>> index = pyndex.Index.from_wrds(db, 2010, "3000")

        """
        if verbose:
            print("Downloading Data ...")
        metadata, stock = alg._download(wrds, year)
        if verbose:
            print(f"Building Russell {index} year {year} ...")
        weights_table = alg._build(stock, year, index,
                                   metadata)

        return weights_table

    @staticmethod
    @dec.typeassert(year=int)
    def get_calendar(year):
        """Generate Russell reconstruction calendar by year.

        Args:
            year (int): Year corresponding to calendar.

        Returns:
            pandas.core.DataFrame: DataFrame containing reconstruction calendar by event.
        """
        calendar = alg._get_calendar(year)
        calendar_table = pd.DataFrame(
            calendar.items(), columns=["event", "date"])
        return calendar_table
