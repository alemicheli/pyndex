from pandas.tseries.offsets import BDay
import pdb
import pandas as pd
import datetime as dt
import calendar
import pyndex.util._decorator as dec
import sys
sys.path.append("../util")

# -------------------Calendar-----------------------


@dec.validatebday(rank_day=True)
def _get_annual_rank(year):
    return dt.date(year, 5, 31)


@dec.validatebday(rank_day=False)
def _get_rebalance(year, quarter):
    month = {2: 6, 3: 9, 4: 12, 1: 3}
    if quarter != 2:
        if quarter == 1:
            year = year+1
        fridays = [week[calendar.FRIDAY]
                   for week in calendar.monthcalendar(year, month[quarter])]
        if fridays[0] == 0:
            return dt.date(year, month[quarter], fridays[3])

        else:
            return dt.date(year, month[quarter], fridays[2])
    else:
        return dt.date(year, month[quarter], max([week[calendar.FRIDAY]
                                                  for week in calendar.monthcalendar(year, month[quarter])]))


@dec.validatebday(rank_day=True)
def _get_quarter_rank(quarter_rebalance):
    preceeding_weeks = 5
    return (quarter_rebalance - dt.timedelta(days=preceeding_weeks*7))


def _get_calendar(year):

    cal = {}
    cal["Annual Rank Day"] = _get_annual_rank(year)
    cal["Annual Rebalance Day"] = _get_rebalance(year, 2)
    cal["Q3 Rebalance Day"] = _get_rebalance(year, 3)
    cal["Q4 Rebalance Day"] = _get_rebalance(year, 4)
    cal["Q1 Rebalance Day"] = _get_rebalance(year, 1)
    cal["Q3 Rank Day"] = _get_quarter_rank(cal["Q3 Rebalance Day"])
    cal["Q4 Rank Day"] = _get_quarter_rank(cal["Q4 Rebalance Day"])
    cal["Q1 Rank Day"] = _get_quarter_rank(cal["Q1 Rebalance Day"])

    return cal


def _match_rank_w_rebalance(cal, year):
    match = {}
    match[cal["Annual Rank Day"]] = cal["Annual Rebalance Day"]
    if year > 2003:
        match[cal["Q3 Rank Day"]] = cal["Q3 Rebalance Day"]
        match[cal["Q4 Rank Day"]] = cal["Q4 Rebalance Day"]
        match[cal["Q1 Rank Day"]] = cal["Q1 Rebalance Day"]
    return match
# -------------------Download-----------------------


def _validate_year(wrds, year):
    last_date = wrds.raw_sql('''SELECT date FROM crsp_a_stock.dsf 
    ORDER BY date DESC LIMIT 1''')["date"].get(0)
    valid_year = (year >= 1989) & (
        _get_quarter_rank(_get_rebalance(year, 1)) <= last_date)
    return valid_year


def _download(wrds, year):
    if not _validate_year(wrds, year):
        raise ValueError(f"Argument year with value {year} not supported")

    stock_query = """
    SELECT date, permco, permno, cusip, prc, shrout, cfacpr FROM crsp_a_stock.dsf
    WHERE date BETWEEN '{rank_y}'
    AND '{rank_y_plus_1}'
    ORDER BY date
    """.format(rank_y=_get_annual_rank(year),
               rank_y_plus_1=_get_annual_rank(year+1))

    stock_table = wrds.raw_sql(stock_query)

    metadata_query = """
    SELECT begdat, permno, hshrcd FROM crsp_a_stock.dsfhdr
    WHERE begdat <= '{rank_y_plus_1}'
    ORDER BY begdat
    """.format(rank_y=_get_annual_rank(year),
               rank_y_plus_1=_get_annual_rank(year+1))

    metadata_table = wrds.raw_sql(metadata_query)

    return metadata_table, stock_table


# -------------------Index-----------------------
def _filter_by_shrcd(stock, metadata):
    common_stocks = metadata[(metadata.hshrcd == 10.0)
                             | (metadata.hshrcd == 11.0)].permno
    return stock[stock.permno.isin(common_stocks)]


def _filter_by_price(stock):
    return stock[(stock["prc"].abs()/stock["cfacpr"] > 1.0)]


def _filter_by_cap(stock):
    return stock[stock["mkt_cap"] > 30e6]


def _filter_by_minimum_requirements(stock):
    return _filter_by_cap(_filter_by_price(stock))


def _filter_by_ranking(stock, index):
    if index == "3000":
        filter_query = 'mkt_cap <= 3000'
    elif index == "2000":
        filter_query = '1000 < mkt_cap <= 3000'
    else:
        filter_query = 'mkt_cap <= 1000'

    ranked_permco = stock.groupby("permco")["mkt_cap"].sum().rank(
        ascending=False).reset_index().query(filter_query).permco

    return stock[stock.permco.isin(ranked_permco)]


def _get_mkt_cap_by_permco(stock):
    return stock.groupby("permco",
                         as_index=False)["mkt_cap"].sum()


def _append_weights(stock):
    mkt_cap_by_permco = _get_mkt_cap_by_permco(stock)
    total_mkt_cap = mkt_cap_by_permco.mkt_cap.sum()
    mkt_cap_by_permco["weights"] = (mkt_cap_by_permco.mkt_cap/total_mkt_cap)
    return stock.merge(mkt_cap_by_permco.drop("mkt_cap", axis=1),
                       on="permco", how="left")


def _get_quarter_dates(quarter, calendar):
    if quarter == 3:
        return calendar["Annual Rank Day"], calendar["Q3 Rank Day"]
    elif quarter == 4:
        return calendar["Q3 Rank Day"], calendar["Q4 Rank Day"]
    else:
        return calendar["Q4 Rank Day"], calendar["Q1 Rank Day"]


def _get_new_IPOs(metadata, calendar, init=None, end=None):
    return metadata[(metadata.begdat > init) & (metadata.begdat <= end)].permno


def _preprocessing_IPOs(metadata, stock, calendar, init=None, end=None):

    IPOs_ids = _get_new_IPOs(metadata, calendar, init=init,
                             end=end)
    IPOs_stock = stock[(stock.permno.isin(IPOs_ids)) &
                       (stock.date == end)]
    filtered_ipos = _filter_by_minimum_requirements(IPOs_stock)
    return filtered_ipos


def _filter_by_capitalization(filtered_ipos, index_stocks, index):
    annual_mkt_cap_by_permco = _get_mkt_cap_by_permco(index_stocks[
        index_stocks["date"] == index_stocks.date.min()])
    min_cap = annual_mkt_cap_by_permco.mkt_cap.min()
    if index == "1000" or index == "3000":
        # Russell 1000 and 3000
        return filtered_ipos[filtered_ipos.mkt_cap >= min_cap]
    else:
        # Russell 2000
        max_cap = annual_mkt_cap_by_permco.mkt_cap.max()
        return filtered_ipos[(filtered_ipos.mkt_cap >= min_cap) &
                             (filtered_ipos.mkt_cap <= max_cap)]


def _filter_by_companies_in_index(filtered_ipos, index_stocks):
    companies_in_index = index_stocks[
        index_stocks["date"] == index_stocks.date.min()].permco.unique()
    return filtered_ipos[~filtered_ipos.permco.isin(companies_in_index)]


def _build_annual_weights(calendar, stock, index, metadata):
    filtered_stocks = _filter_by_minimum_requirements(
        stock[stock.date == calendar["Annual Rank Day"]])
    filtered_stocks = _filter_by_shrcd(filtered_stocks, metadata)
    filtered_stocks = _filter_by_ranking(filtered_stocks, index)
    return _append_weights(filtered_stocks)


def _build_quarterly_weights(index_stocks, metadata, stock,
                             calendar, index, quarter):
    init, end = _get_quarter_dates(quarter, calendar)
    filtered_ipos = _preprocessing_IPOs(metadata, stock, calendar,
                                        init=init, end=end)
    filtered_ipos = _filter_by_shrcd(filtered_ipos, metadata)
    filtered_ipos = _filter_by_capitalization(filtered_ipos,
                                              index_stocks, index)
    filtered_ipos = _filter_by_companies_in_index(filtered_ipos,
                                                  index_stocks)
    new_index_permnos = filtered_ipos.permno.append(index_stocks.permno,
                                                    ignore_index=True)
    new_index_composition = stock[(stock.date == end) &
                                  (stock.permno.isin(new_index_permnos))]

    return pd.concat([index_stocks, _append_weights(new_index_composition)])

# ----------------- Formatting -----------------------


def _beautify_table(table, calendar, year):
    table.date = table.date.replace(
        to_replace=_match_rank_w_rebalance(calendar, year))
    weights_table = pd.pivot_table(table,  values='weights', index=['date'],
                                   columns=['permno', 'cusip', 'permco'])
    return weights_table


def _reindex_with_bday(weights_table, trading_days, calendar, year):
    last_bday = _get_calendar(year+1)["Annual Rebalance Day"] - BDay(1)
    trading_days = pd.to_datetime(trading_days)
    index_from_rebalance = trading_days[trading_days.date >=
                                        calendar["Annual Rebalance Day"]]
    new_index = index_from_rebalance.append(
        pd.bdate_range(trading_days[-1] + BDay(1), last_bday))
    return weights_table.reindex(new_index).fillna(method="ffill").fillna(0)


def _build(stock, year, index, metadata):

    calendar = _get_calendar(year)
    stock = stock.assign(mkt_cap=stock.prc.abs()*stock.shrout*1000)
    index_stocks = _build_annual_weights(calendar,
                                         stock, index, metadata)
    if year > 2003:
        for quarter in [3, 4, 1]:
            index_stocks = _build_quarterly_weights(
                index_stocks, metadata, stock, calendar,
                index, quarter)
    weights_table = _beautify_table(index_stocks, calendar, year)
    return _reindex_with_bday(weights_table, stock.date.unique(), calendar, year)
