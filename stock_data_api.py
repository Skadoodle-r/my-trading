# 导入必要的库
import requests

# 定义获取股票数据的函数
def get_stock_data(symbol, start_date, end_date):
    # 这里使用一个示例API，实际使用时需要替换为真实可用的API
    api_url = f'https://api.example.com/stock/{symbol}?start_date={start_date}&end_date={end_date}'
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# 示例调用
if __name__ == '__main__':
    symbol = 'AAPL'
    start_date = '2023-01-01'
    end_date = '2023-12-31'
    data = get_stock_data(symbol, start_date, end_date)
    if data:
        print(data)
    else:
        print('Failed to get stock data.')