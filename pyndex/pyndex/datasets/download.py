from .sql_query import _get_sql_query


def _get_dataset(wrds_connection, start_year, end_year, frequency, type=None):
    """Gets the pandas DataFrames from SQL query in WRDS.
    
    Args:
        wrds_connection (wrds.sql.Connection): WRDS SQL Connection used to download the data.
        start_year (str): Initial date of data.
        end_year (str): End date of data.
        frequency (str): Frequency of update WRDS stock files.
        type (str, optional): Flag for body/header files. Defaults to None.
    
    Returns:
        pandas.DataFrame: DataFrame containing the data.
    """
    return wrds_connection.raw_sql(
        _get_sql_query(
            start_year=start_year, end_year=end_year, frequency=frequency, type=type
        )
    )


def _download_data(wrds_connection, start_year, end_year, frequency):
    """Wrapper for data download. 
    
    Args:
        wrds_connection (wrds.sql.Connection): WRDS SQL Connection used to download the data.
        start_date ([type]): Initial date of data.
        end_date ([type]): Final date of data.
        frequency ([type]): Frequency of update WRDS stock files.
    
    Returns:
         pandas.DataFrame: Body and Header Pandas DataFrame containing Stock data.
    """
    return (
        _get_dataset(wrds_connection, start_year, end_year, frequency, type="header"),
        _get_dataset(wrds_connection, start_year, end_year, frequency, type="body"),
    )

