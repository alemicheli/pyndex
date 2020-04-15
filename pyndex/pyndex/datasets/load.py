import sys
from .download import _download_data
import pathlib


def _has_connection(wrds_connection):
    """Checks if the input is a WRDS SQL Connection.
    
    Args:
        wrds_connection (wrds.sql.Connection): WRDS SQL Connection to download data.
    
    Raises:
        TypeError: If type is not wrds.sql.Connection raise error.
    """
    import wrds

    if type(wrds_connection) != wrds.sql.Connection and wrds_connection is not None:
        raise TypeError("Wrong type for connection to WRDS.")
    else:
        return True


def load_data(wrds_connection, start_year="1989", frequency="a", end_year=None):
    """Load Stock data for index construction.
    
    Args:
        wrds_connection (wrds.sql.Connection, optional): WRDS Sql connection from the WRDS python package. Defaults to None.
        start_year (str, optional): Initial year for downloaded data. Defaults to "1989".
        frequency (str, optional): WRDS frequency for stock files. Possible choices are 
                                    "m", "q" and "a" for monthly, quarterly and annually.
                                   The availability of data depends on user subscription.
                                    Defaults to "a".
        end_year (str, optional): Final year for downloaded data. If None returns
                                     most recent available data. Defaults to None.
    
    Returns:
        2 pandas.DataFrame : (header, body) dataframes.
    """

    if wrds_connection is None:
        raise ValueError("No existing filename nor WRDS Connection.")

    if wrds_connection is not None and _has_connection(wrds_connection):
        print("Downloading Data from WRDS.")
        return _download_data(wrds_connection, start_year, end_year, frequency)

