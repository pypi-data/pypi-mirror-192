import ta
import pandas as pd
import numpy as np


#Main indicator strategy
def highest(data, length):
    return np.array( [0]*length + [ np.max(data[i-length+1: i+1]) for i in range(length, len(data))])

def lowest(data, length):
    return np.array( [0]*length + [ np.min(data[i-length+1: i+1]) for i in range(length, len(data))])

def tr(high, low, close):
    hl = np.abs(high-low)
    hc = np.abs(high-close.shift())
    lc = np.abs(low-close.shift())
    ranges = pd.concat([hl, hc, lc], axis=1)
    tr = np.max(ranges, axis=1)
    return pd.Series(tr)

class Indicators:
    
    def __init__(self, df):
        # Trend
        self.buy, self.sell =  None , None
        self.trend_ind(df)
        # SuperTrend
        self.trend, self.trend_start_price = None, None
        self.sup_buy, self.sup_sell = None, None
        self.supertrend_ind(df)
        
    def get_trend_buy(self):
        return self.buy
    
    def get_trend_sell(self):
        return self.sell
    
    def get_supertrend_buy(self):
        return self.sup_buy
    
    def get_supertrend_sell(self):
        return self.sup_sell
    
    def get_trend(self):
        return self.trend
    
    def get_trend_start_price(self):
        return self.trend_start_price
    
    def trend_ind(self, df):
        high, low, close = pd.Series(df.high),pd.Series(df.low), pd.Series(df.close)

        Lowest_Low = lowest(low, 3)
        MA_Low = ta.trend.ema_indicator(low, 3, fillna=True)

        Highest_High = highest(high, 2)
        MA_High = ta.trend.sma_indicator(high, 2, fillna=True)

        #ATR_Half = ta.volatility.average_true_range(high, low, close, 100, fillna=True) / 2
        atr10 = ta.volatility.average_true_range(high, low, close, 10, fillna=True)

        ema50 = ta.trend.ema_indicator(close, 50, fillna=True)
        ema200 = ta.trend.ema_indicator(close, 200, fillna=True)
        sma100 = ta.trend.sma_indicator(close, 100, fillna=True)

        Next_Trend = [0]
        Trend = [0]
        Low_Max = [low[0]]
        High_Min = [high[0]]
        Line_HT = [close[0]]
        Arrow_Shift = [0.0]
        buy = [False]*len(df)
        sell = [False]*len(df)
        for i in range(1, len(close)):
            Next_Trend_ = Next_Trend[i-1]
            Trend_ = Trend[i-1]
            Low_Max_ = Low_Max[i-1]
            High_Min_ = High_Min[i-1]
            Line_HT_ = Line_HT[i-1]
            Arrow_Shift_ = Arrow_Shift[i-1]

            if Next_Trend_ == 1:
                Low_Max_ = max(Low_Max_, Lowest_Low[i])
                if MA_High[i] < Low_Max_ and close[i] < low[i-1]:
                    Trend_ = 1
                    Next_Trend_ = 0
                    High_Min_ = Highest_High[i]

            if Next_Trend_ == 0:
                High_Min_ = min(High_Min_, Highest_High[i])
                if MA_Low[i] > High_Min_ and close[i] > high[i-1]:
                    Trend_ = 0
                    Next_Trend_ = 1
                    Low_Max_ = Lowest_Low[i]
            
            if Trend_ == 0:
                if Trend[i-1] == 0:
                    Line_HT_ = max(Low_Max_, Line_HT[i-1])
                if Trend[i-1] == 1:
                    Arrow_Shift_ = -1 * atr10[i]

            if Trend_ == 1:
                if Trend[i-1] == 1:
                    Line_HT_ = min(High_Min_, Line_HT[i-1])
                if Trend[i-1] == 0:
                    Arrow_Shift_ = 1 * atr10[i]

            Next_Trend.append(Next_Trend_)
            Trend.append(Trend_)
            Low_Max.append(Low_Max_)
            High_Min.append(High_Min_)
            Line_HT.append(Line_HT_)
            Arrow_Shift.append(Arrow_Shift_)

            if Arrow_Shift_ < 0 and Arrow_Shift[i-1] >= 0:
                buy[i] = True
            elif Arrow_Shift_ > 0 and Arrow_Shift[i-1] <= 0:
                sell[i] = True
        self.buy = buy
        self.sell = sell
        
    
    def supertrend_ind(self, df):
        high, low, close = pd.Series(df.high),pd.Series(df.low), pd.Series(df.close)
        Periods = 10
        src = (high+low)/2
        Multiplier = 3.0
        changeATR= True
        showsignals = True
        highlighting = True
        atr2 = ta.trend.sma_indicator(tr(high, low, close), Periods, True)
        atr= ta.volatility.average_true_range(high, low, close, Periods, True) if changeATR else atr2

        up, dn = [0], [0]
        trend = [1]
        start_price = [0]
        trend_curr_price = [0]
        buy, sell = [False], [False]
        for i in range(1, len(close)):
            up_=src[i]-(Multiplier*atr[i])
            up1 = up[i-1]
            up.append(max(up_,up1) if close[i-1] > up1 else up_ )
            dn_ = src[i]+(Multiplier*atr[i])
            dn1 = dn[i-1]
            dn.append(min(dn_, dn1) if close[i-1] < dn1 else dn_)
            
            trend.append(1 if trend[i-1]==-1 and close[i] > dn1 else -1 if trend[i-1]==1 and close[i] < up1 else trend[i-1])

            buySignal = trend[i] == 1 and trend[i-1] == -1
            sellSignal = trend[i] == -1 and trend[i-1] == 1
            
            start_price.append(high[i] if buySignal or sellSignal else start_price[i-1])
            trend_curr_price.append(dn[-1] if trend[-1] == -1 else up[-1])
            buy.append(buySignal)
            sell.append(sellSignal)
        
        self.sup_buy, self.sup_sell = buy, sell
        self.trend = trend
        self.trend_start_price = start_price
        self.trend_curr_price = trend_curr_price
