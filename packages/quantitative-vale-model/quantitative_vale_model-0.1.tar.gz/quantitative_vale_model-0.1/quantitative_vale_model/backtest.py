from .strategy import ValeStrategy
import backtrader as bt
import yfinance as yf
import pandas
from datetime import date

def backtest(start_data=None):
    '''
    Call this function to backtest the strategy results passing the date when you want the backtest starts
    Args:
        start_data (String): init date to the backtest (%Y-%m-%d).
    '''
    if not start_data:
          raise ValueError('Retrieve a data in string format %Y-%m-%d')

    date_today = date.today().strftime('%Y-%m-%d')

    data = yf.download('VALE3.SA', start=start_data, end=date_today)

    cerebro = bt.Cerebro()

    data_feed = bt.feeds.PandasData(dataname=data)
    cerebro.adddata(data_feed)

    cerebro.addstrategy(ValeStrategy)
    cerebro.addsizer(bt.sizers.FixedSize, stake=100)


    results = cerebro.run()

    total_return = (cerebro.broker.getvalue() / 10000 - 1) 
    days = (data.index[-1] - data.index[0]).days
    anually_retrn = (total_return + 1) ** (365 / days) - 1
    

    return f'Retorno percentual total: {total_return*100}%, com retorno anualizado de {anually_retrn*100}%'


def trade_action():
    '''
    Call this function trade_action to see what the model say for the next movements
    
    '''
    df = yf.Ticker('VALE3.SA').history('100d')
    sma_period_short = df['Close'].rolling(window=20).mean().iloc[-1]
    sma_period_long = df['Close'].rolling(window=50).mean().iloc[-1]
    sma_volume = df['Volume'].rolling(window=80).mean().iloc[-1]
    actual_volume = df['Volume'].iloc[-1]


    if sma_period_short > sma_period_long and actual_volume > sma_volume * 1.1:
        return 'buy'
    elif sma_period_short < sma_period_long:
        return 'sell'
     