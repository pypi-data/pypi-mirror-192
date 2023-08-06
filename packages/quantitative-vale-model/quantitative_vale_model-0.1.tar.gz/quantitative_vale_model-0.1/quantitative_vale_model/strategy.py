import backtrader as bt
import backtrader.indicators as btind


class ValeStrategy(bt.Strategy):
    params = dict(
        sma_period_short=20,
        sma_period_long=50
    )

    def __init__(self):
        self.sma_short = btind.SMA(period=self.params.sma_period_short)
        self.sma_long = btind.SMA(period=self.params.sma_period_long)
        self.sma_volume = btind.SMA(self.data.volume, period=80)

    def next(self):
        if not self.position:  
            if self.sma_short > self.sma_long and self.data.volume[0] > self.sma_volume[0] * 1.1:
                self.buy()
        elif self.sma_short < self.sma_long:
            self.sell()