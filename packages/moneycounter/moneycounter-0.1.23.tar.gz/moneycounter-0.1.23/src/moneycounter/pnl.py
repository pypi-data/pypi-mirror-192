from datetime import date, datetime
import pandas as pd
from .dt import our_localize
from .dt import day_start_next_day, day_start
from .str_utils import is_near_zero


def realized_trades(trades_df):
    """
    :param df:  Pandas dataframe with single account and ticker.
    :return: realized_df Pandas dataframe of realized trades.
    """

    df = trades_df.copy()

    buy_sum = df.where(df.q >= 0).q.sum()
    sell_sum = -df.where(df.q < 0).q.sum()
    delta = buy_sum - sell_sum

    # Start
    if buy_sum == sell_sum:
        realized_df = df
    if buy_sum > sell_sum:
        last_i = df.where(df.q < 0).index[-1]
        realized_df = df.head(last_i + 1)

        # A short loop to reduce last sell trades by delta
        for j in range(last_i, -1, -1):
            rec = realized_df.loc[j]
            q = rec.q
            if q > 0:
                if delta > q:
                    delta -= q
                    realized_df.at[j, 'q'] = 0
                else:
                    realized_df.at[j, 'q'] -= delta
                    break

    elif sell_sum > buy_sum:
        last_i = df.where(df.q >= 0).index[-1]
        realized_df = df.head(last_i + 1)

        # A short loop to reduce last sell trades by delta
        for j in range(last_i, -1, -1):
            rec = realized_df.loc[j]
            q = rec.q
            if q < 0:
                if delta < q:
                    delta -= q
                    realized_df.at[j, 'q'] = 0
                else:
                    realized_df.at[j, 'q'] -= delta
                    break

    realized_df.reset_index(drop=True, inplace=True)
    return realized_df


def pnl_calc(df, price=None):
    '''
    :param df:  Trades data frame
    :return: profit or loss
    '''
    if df.empty:
        return 0

    pnl = (-df.q * df.p).sum()
    if price:
        pnl += df.q.sum() * price

    cs = df.cs.iloc[0]
    pnl *= cs

    return pnl


def pnl(df, price=0):
    """
    Calculate FIFO PnL

    :param df: Pandas dataframe with single account and ticker
    :param price:     Closing price if there are unrealized trades
    :return:          realized pnl, unrealized pnl, total

    IMPORTANT NOTE: The default value for price of zero is only useful when there is no open position.
    """
    realized_df = realized_trades(df)
    realized_pnl = pnl_calc(realized_df)
    total = pnl_calc(df, price=price)
    unrealized_pnl = total - realized_pnl

    return realized_pnl, unrealized_pnl, total


# def wap_old(data):
#     """
#     weighted_average_price(t, a) - query db values q,p and calculate wap
#     get_balances(d, a, t) - query trades and cash,  calculate cash realized contributions, balances[k]=v
#     valuations(d, account, ticker) - use get_balances() for query - for each pos get price and value it.
#
#     These two functions get everything even if pos is zero or no trades in date range.
#     get_futures_pnl(a, d) - query trade sums and return [[t, p, pos, pnl]], total
#     get_equities_pnl(a, d) - same as get_futures_pnl but just equities
#     """
#
#     n = len(data)
#
#     #  close out lifo trades
#     for i in range(1, n):
#         (q, p) = data[i]
#         for j in range(i - 1, -1, -1):
#             q2 = data[j][0]
#             if q * q2 >= 0.0:
#                 continue
#             if abs(q) <= abs(q2):
#                 q2 += q
#                 q = 0
#             else:
#                 q += q2
#                 q2 = 0
#             data[j][0] = q2
#             if is_near_zero(q):
#                 break
#         data[i][0] = q
#
#     # Calculate WAP
#     pqsum = 0.0
#     qsum = 0.0
#     for x in data:
#         (q, p) = x
#         pqsum += p * q
#         qsum += q
#
#     if 0 == is_near_zero(qsum):
#         wap = pqsum / qsum
#     else:
#         wap = 0.0
#     return qsum, wap


# def wap_calc_first_attempt(df, price):
#     '''
#     total based on unrealized trades
#     total = cs * pos * (price - wap)
#     wap = price - total / cs / pos
#
#     :param df: trades
#     :return: wap
#     '''
#
#     if df.empty:
#         return 0.0
#
#     pos = df.q.sum()
#     if pos == 0:
#         return 0.0
#
#     realized_pnl, unrealized_pnl, total = pnl(df, price=price)
#     cs = df.cs.iloc[0]
#     wap = -unrealized_pnl / cs / pos
#
#     return wap


def remove_old_trades(df):
    """
    Remove all trades before the last time the position changed sign.


    :param df:
    :return:
    """
    df['qsum'] = df.q.cumsum()
    pos = df.qsum.iat[-1]

    if is_near_zero(pos):
        df = df.head(0)
    else:
        try:
            # Eliminate all rows since the last time the pos was negative.
            if pos > 0:
                i = df[df.qsum <= 0][-1:].index[0]
            else:
                i = df[df.qsum >= 0][-1:].index[0]

            if is_near_zero(df.qsum[i]):
                i += 1

            df = df[i:]
            df.reset_index(drop=True, inplace=True)

            df.loc[0].q = df.qsum[0]
        except IndexError:
            # Nothing to eliminate
            pass

        df = df.drop(columns='qsum', axis=1)

    return df


def wap_calc(df):
    """

    Equivalent entry price given the current position was acquired at once.
    Should work for short position too.
    Formula: cost_basis / position

    :param df:
    :return wap:

    """

    position = df.q.sum()
    if is_near_zero(position):
        return 0.0

    df = df[['q', 'p']].copy()
    df = remove_old_trades(df)

    # Eliminate all trades before last

    pos_flags = df.q >= 0
    if position > 0:
        # Remove negative trades
        df = df[pos_flags]
    else:
        # Remove positive trades
        df = df[~pos_flags]

    df.reset_index(drop=True, inplace=True)

    qp = df.q.dot(df.p)
    qsum = df.q.sum()

    wap = abs(qp / qsum)

    return wap


def fifo(dfg, dt):
    """
    Calculate realized gains for sells later than d.
    THIS ONLY WORKS FOR TRADES ENTERED AS LONG POSITIONS
    Loop forward from bottom
       0. Initialize pnl = 0 (scalar)
       1. everytime we hit a sell
          a. if dfg.dt > dt: calculate and add it to pnl
          b. reduce q for sell and corresponding buy records.
    """

    def realize_q(n, row):
        pnl = 0
        quantity = row.q
        add_pnl = row['dt'] >= dt
        cs = row.cs
        price = row.p

        for j in range(n):
            buy_row = dfg.iloc[j]
            if buy_row.q <= 0.0001:
                continue

            q = -quantity
            if buy_row.q >= q:
                adj_q = q
            else:
                adj_q = buy_row.q

            if add_pnl:
                pnl += cs * adj_q * (price - buy_row.p)

            dfg.at[j, 'q'] = buy_row.q - adj_q
            quantity += adj_q
            dfg.at[n, 'q'] = quantity

            if quantity > 0.0001:
                break

        return pnl

    realized = 0
    dfg.reset_index(drop=True, inplace=True)
    for i in range(len(dfg)):
        row = dfg.iloc[i]
        if row.q < 0:
            pnl = realize_q(i, row)
            realized += pnl

    return realized


def stocks_sold(trades_df, year):
    # Find any stock sells this year
    t1 = day_start(date(year, 1, 1))
    t2 = day_start_next_day(date(year, 12, 31))
    mask = (trades_df['dt'] >= t1) & (trades_df['dt'] < t2) & (trades_df['q'] < 0)
    sells_df = trades_df.loc[mask]
    return sells_df


def realized_gains_fifo(trades_df, year):
    #
    # Use this to find realized pnl for things sold this year
    #
    dt = our_localize(datetime(year, 1, 1))
    sells_df = stocks_sold(trades_df, year)
    a_t = sells_df.loc[:, ['a', 't']]
    a_t = a_t.drop_duplicates()

    # get only trades for a/t combos that had sold anything in the given year
    df = pd.merge(trades_df, a_t, how='inner', on=['a', 't'])

    # df['d'] = pd.to_datetime(df.dt).dt.date
    realized = df.groupby(['a', 't']).apply(fifo, dt).reset_index(name="realized")

    return realized


def realized_gains_one(trades_df, year):
    trades_df.reset_index(drop=True, inplace=True)
    t = day_start(date(year, 1, 1))
    df = trades_df[trades_df.dt < t]
    realized_prior, _, _ = pnl(df)

    t = day_start_next_day(date(year, 12, 31))
    df = trades_df[trades_df.dt < t]
    realized, _, _ = pnl(df)

    result = realized - realized_prior

    return result


def stocks_traded(trades_df, year):
    # Find any stock sells this year
    t1 = day_start(date(year, 1, 1))
    t2 = day_start_next_day(date(year, 12, 31))
    mask = (trades_df['dt'] >= t1) & (trades_df['dt'] < t2)
    traded_df = trades_df.loc[mask]
    return traded_df


def realized_gains(trades_df, year):
    traded_df = stocks_traded(trades_df, year)
    traded_df = traded_df.loc[:, ['a', 't']]
    traded_df = traded_df.drop_duplicates()

    # get only trades for a/t combos that had sold anything in the given year
    df = pd.merge(trades_df, traded_df, how='inner', on=['a', 't'])

    if df.empty:
        pnl = pd.DataFrame(columns=['a', 't', 'realized'])
    else:
        pnl = df.groupby(['a', 't']).apply(realized_gains_one, year).reset_index(name="realized")

        # Eliminate zeros
        pnl = pnl.loc[pnl.realized != 0]
        pnl.reset_index(drop=True, inplace=True)

    return pnl
