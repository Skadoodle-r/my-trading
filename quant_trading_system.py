# 导入必要的库
import pandas as pd
import numpy as np
import stock_data_api

# 定义双均线策略函数
def double_moving_average_strategy(data, short_window, long_window):
    # 计算短期和长期均线
    data['short_ma'] = data['close'].rolling(window=short_window).mean()
    data['long_ma'] = data['close'].rolling(window=long_window).mean()
    # 生成买卖信号
    data['signal'] = 0.0
    data['signal'][short_window:] = np.where(data['short_ma'][short_window:] > data['long_ma'][short_window:], 1.0, 0.0)
    data['position'] = data['signal'].diff()
    return data

# 定义资金管理和交易执行类
class Portfolio:
    def __init__(self, initial_capital):
        self.capital = initial_capital
        self.positions = 0

    def execute_trade(self, signal, price):
        if signal == 1:
            # 买入
            if self.capital > 0:
                self.positions = self.capital / price
                self.capital = 0
        elif signal == -1:
            # 卖出
            if self.positions > 0:
                self.capital = self.positions * price
                self.positions = 0
        return self.capital, self.positions

# 模拟数据
if __name__ == '__main__':
    # 生成示例数据
    # dates = pd.date_range(start='2023-01-01', periods=100)
    # close_prices = np.random.randn(100).cumsum() + 100
    # data = pd.DataFrame({'close': close_prices}, index=dates)
    # 调用股票数据获取接口
    symbol = 'AAPL'
    start_date = '2023-01-01'
    end_date = '2023-12-31'
    stock_data = stock_data_api.get_stock_data(symbol, start_date, end_date)
    if stock_data:
        data = pd.DataFrame(stock_data)
        # 假设返回的数据包含 'close' 列
        if 'close' in data.columns:
            data.index = pd.to_datetime(data.index)
        else:
            print('Data does not contain 'close' column.')
    else:
        print('Failed to get stock data.')
    # 调用双均线策略函数
    short_window = 5
    long_window = 20
    result = double_moving_average_strategy(data, short_window, long_window)
    # 初始化资金管理
    portfolio = Portfolio(initial_capital=100000)
    # 执行交易
    for i in range(len(result)):
        signal = result['position'].iloc[i]
        price = result['close'].iloc[i]
        capital, positions = portfolio.execute_trade(signal, price)
        result.at[result.index[i], 'capital'] = capital
        result.at[result.index[i], 'positions'] = positions
    print(result)