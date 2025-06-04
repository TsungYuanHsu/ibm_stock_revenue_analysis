import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import plotly.io as pio
pio.renderers.default = "iframe"

import warnings
# Ignore all warnings
warnings.filterwarnings("ignore", category=FutureWarning)


def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021-06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()
    from IPython.display import display, HTML
    fig_html = fig.to_html()
    display(HTML(fig_html))

# Use yfinance library to scrap tesla historical stock data
tesla = yf.Ticker('TSLA')

tesla_stock = tesla.history(period='max')
tesla_stock.reset_index(inplace=True)
print(f'Here is the first 5 rows of tesla stock data \n {tesla_stock.head()}')

# Use beautifulsoup library to scrap tesla historical revenue data and make dataframe structure
r = requests.get('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm')
print(f'The status code is {r.status_code}')
html_data = r.text

soup = BeautifulSoup(html_data, 'html.parser')
tables = soup.find_all('tbody')
revenue_table = tables[1]
rows = revenue_table.find_all('tr')

revenue_list = []
for row in rows:
    dict = {}
    date = row.find_all('td')[0].text
    revenue = row.find_all('td')[1].text
    dict['Date'] = date
    dict['Revenue'] = revenue
    revenue_list.append(dict)

tesla_revenue = pd.DataFrame(revenue_list)
# print(tesla_revenue.head())

tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(r',|\$',"", regex=True)
tesla_revenue.dropna(inplace=True)
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]
print(f'Here is the last 5 rows of tesla revenue data \n {tesla_revenue.tail()}')

# Use yfinance library to scrap gme historical stock data
gme = yf.Ticker('GME')

gme_stock = gme.history(period='max')
gme_stock.reset_index(inplace=True)
print(f'Here is the first 5 rows of gme stock data \n {gme_stock.head()}')

# Use beautifulsoup library to scrap gme historical revenue data and make dataframe structure
r2 = requests.get('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html')
print(f'The status code is {r2.status_code}')
html_data_2 = r2.text

soup_2 = BeautifulSoup(html_data_2, 'html.parser')
tables_2 = soup_2.find_all('tbody')
revenue_table_2 = tables_2[1]
rows_2 = revenue_table_2.find_all('tr')

revenue_list_2 = []
for row in rows_2:
    dict_2 = {}
    date = row.find_all('td')[0].text
    revenue = row.find_all('td')[1].text
    dict_2['Date'] = date
    dict_2['Revenue'] = revenue
    revenue_list_2.append(dict_2)

gme_revenue = pd.DataFrame(revenue_list_2)
# print(gme_revenue.head())

gme_revenue["Revenue"] = gme_revenue['Revenue'].str.replace(r',|\$',"", regex=True)
gme_revenue.dropna(inplace=True)
gme_revenue = gme_revenue[gme_revenue['Revenue'] != ""]
print(f'Here is the last 5 rows of gme revenue data \n {gme_revenue.tail()}')


make_graph(tesla_stock, tesla_revenue, 'TESLA stock')
make_graph(gme_stock, gme_revenue, 'GameStop')