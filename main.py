"""
Convert requried columns into the edgewonk column names
Column names and indexing will have to be in order
Since closed date is a mandatory field will have to also take in thw secondary order position .csv file
"""

import pandas as pd
import numpy as np
import datetime as dt
import time

desired_width=320
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns',15)

TradeHistory = 'BybitTradeHistoryUSDTPerpetual20220223-20220516'
ClosedPnL = 'BybitClosedPNLUSDTPerpetual20220223-20220516'
ClosedPnLdf = pd.read_csv(ClosedPnL+'.csv')
TradeHistorydf = pd.read_csv(TradeHistory+'.csv')

def Rename_ClosedPnL():
    ClosedPnLRenameddf = ClosedPnLdf.rename(columns={
        "Trade Time(UTC+0)":"Closing Time",
        "Closing Direction":"Type[buy/sell]",
        "Qty":"Size / Quantity",
        "Exit Price": "Closing Price",
        "Closed P&L": "Net Profit",
        "Contracts": "Symbol"

    })
    ClosedPnLRenameddf.to_csv("ClosedPnL.csv")
    # print(ClosedPnLRenameddf)
    #Create mappings of columns to be renamed
    #Required fields:
    # Opening Time, Type [buy/sell], symbol, setup, Size /Quantity, Closing Time
    #Entry Price, Closing price, Swap, Commission, Net Profit
"""
From closed PnL [ClosedPnLdf] sheet we get
Contracts -> Symbol DONE
Closing Direction ->Type[buy/sell] DONE
Qty -> Size / Quantity DONE
Entry Price -> Entry Price NO CHANGE
Exit Price -> Closing Price DONE
Closed P&L -> Net Profit DONE
Trade Time(UTC+10) -> Closing Time DONE
"""

def Rename_TradeHistory():
    TradeHistoryRenameddf = TradeHistorydf.rename(columns={
        "Transaction Time(UTC+0)":"Opening Time",
        "Contracts": "Symbol"
    })
    # print(TradeHistoryRenameddf.head(5))
    TradeHistoryRenameddf.to_csv("TradeHistoryPre.csv")



def MergeHistoryOrders(TradeHistoryRenameddf):
    """Sum Size / Quantity for each contract within same datetime"""
    "PENIUS"
    TradeHistoryRenameddf = pd.read_csv("TradeHistoryPre.csv",parse_dates=['Opening Time'])
    TradeHistoryFiltered = (TradeHistoryRenameddf['Filled Type'] == 'Trade')
    TradeHistoryFiltered = TradeHistoryRenameddf.loc[TradeHistoryFiltered]
    print(TradeHistoryFiltered)

    OrderGroup = TradeHistoryFiltered.groupby(['Order No.'])
    df1 = TradeHistoryFiltered.groupby(['Order No.','Opening Time','Symbol'])['Filled Qty'].sum()
    # df1.to_csv('TradeHistory.csv')
    df2 = pd.read_csv("TradeHistory.csv", parse_dates=['Opening Time'],index_col="Opening Time")
    # df2.rename(columns={"Opening Time":"OpeningTime"})
    print(df2)
    # print(df2)
    print(df2['Order No.'])

    OrderList = TradeHistoryFiltered['Order No.'].tolist()
    Unique = set(OrderList)
    OrderList = list(Unique)


    """For each order No sum QTY and take first Opening Time"""
    df2.rename(columns={0:"Zibi"}, inplace=True)
    df2.to_csv('OpeningTime.csv')
    # df2.columns = ['OpeningTime', 'OrderNo.', 'Symbol', 'FilledQty']
    print(df2)
    df2.to_csv('OpeningTime.csv')
    # print(type(df2['OpeningTime']))
    df_Resampled = df2.OpeningTime.resample('10T').sum()
    print(df_Resampled)
    df2 = df2.groupby(['Order No.','Symbol','Opening Time'])['Filled Qty'].sum()


    # for i in OrderList:
    #     # df2 = df2.loc[df2.apply(lambda x: x.OrderNo in OrderList, axis=1)]
    #     df3 = df2['Order No.'] == i
    #     df4 = df2.loc[df3]
    #     df5 = pd.concat([df4,df3])
    #     print(df4)
        # x = x+1
        # print(df3)
        # df2 = df2[df2['Order No.']].isin(OrderList)
        # print(df2)




def MergePnLANDTradeHistory():
    MergedHistorydf = pd.read_csv("TradeHistory.csv", parse_dates=['Opening Time'])
    ClosedPnLdf = pd.read_csv("ClosedPnL.csv", parse_dates=['Closing Time'])




    SymbolList = TradeHistoryFiltered['Symbol'].tolist()
    Unique = set(SymbolList)
    SymbolList = list(Unique)
    # """Create a unique list of Symbols to match using apply but grouping by Date a(Include Qty to enable merge), this way we obtain all unique symbol trades"""
    #

    # df1 = OrderGroup['Filled Qty'].sum
    # df1
    #
    # g = TradeHistoryFiltered.groupby('Order No.')['Symbol','Opening Time']
    # print(g)
    # print(df1)



    # ClosedPnLRenameddf = pd.read_csv("ClosedPnL.csv")
    # TradeHistoryRenameddf['test'] = pd.to_datetime(TradeHistoryRenameddf['Opening Time'])
    # print(new)
    # print(ClosedPnLRenameddf.head(5))
    # for state, frame in g:
    #     ...
    #     print(f"First 2 entries for {state!r}")
    # ...
    # print("------------------------")
    # ...
    # print(g.head(2), end="\n\n")

    # print(type(g))
    # print(g)
    # df = g.apply(lambda x: x[['Filled Qty'].sum()])
    # df.to_csv("test.csv")
    # print(df)
    # df_out = TradeHistoryRenameddf.groupby(['Symbol', pd.Grouper(key='Order No.')])
    # print(df_out)
    # df_out2 = TradeHistoryRenameddf.groupby("Filled Qty").sum()
    # print(df_out2)
    # print(df_out)
    # df_out.to_csv("TradeHistory.csv")
    # print(df_out)
    # CompiledTradeHistory = TradeHistoryRenameddf


Rename_ClosedPnL()
Rename_TradeHistory()
MergeHistoryOrders(TradeHistorydf)
# MergeHistoryOrders(TradeHistorydf)
# .last()
# .reset_index()
# ).replace([None], [np.nan]))