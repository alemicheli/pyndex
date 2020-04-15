def _correct_frequency(frequency):
    """Checks if frequency is of the right format for WRDS files: crsp_{frequency}.dsf
    
    Args:
        frequency (str): Frequency for the stock files. Allowed frequencies are "m", "q" and "a" for 
                        monthly, quarterly or annually updated files.
    
    Returns:
        bool: Correct/Incorrect frequency.
    """
    return (frequency == "q") or (frequency == "m") or (frequency == "a")


def _get_sql_query(start_year, end_year, frequency, type=None):
    """Generates the SQL query to download the data.
    
    Args:
        start_year (str): Initial year for data.
        end_year (str): Final year for data.
        frequency (str): Update Frequency for WRDS files. 
        type (str, optional): Flag for header or body files. Defaults to None.
    
    Raises:
        ValueError: Wrong input frequency.
    
    Returns:
        str: Formatted SQL query for WRDS.
    """
    if not _correct_frequency(frequency):
        raise ValueError(
            "Wrong identifier for frequency file. Available Identifiers : 'a', 'm' , 'q'"
        )

    if type == "header":
        sql_query_header = """
        SELECT * FROM crsp_{frequency}_stock.dsfhdr
        ORDER BY begdat
        """
        return sql_query_header.format(frequency=frequency)
    else:
        sql_query_body = """SELECT shrout, permco, prc, permno, cusip, ret, date FROM crsp_{frequency}_stock.dsf
        WHERE date BETWEEN '01-May-{start_year}'
        AND '01-June-{end_year}'
        ORDER BY date"""
    return sql_query_body.format(
        start_year=start_year, end_year=end_year, frequency=frequency
    )
