!pip install yfinance
!pip install bs4
!pip install nbformat


import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings


# Ignore all warnings
warnings.filterwarnings("ignore", category=FutureWarning)
# we define a function to  make a graph


def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()

####Use yfinance to Extract Stock Data#######

tsla_ticker = yf.Ticker("TSLA")
tsla_ticker
tesla_data=tsla_ticker.history(period="max")
tesla_data
tesla_data.reset_index(inplace=True)
print(tesla_data.head())
##Use Webscraping to Extract Tesla Revenue Data####
html_url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
response = requests.get(html_url)
html_data = response.content
soup = BeautifulSoup(html_data, "html.parser")
###Using BeautifulSoup or the read_html function extract the table with Tesla Revenue
###and store it into a dataframe named tesla_revenue. The dataframe should have columns Date and Revenue.
tables = soup.find_all('table')
relevant_table = None
for table in tables:
    if "Tesla Quarterly Revenue" in table.text:
        relevant_table = table
        
data = []
if relevant_table:
    rows = relevant_table.find_all('tr')
    for row in rows[1:]:  
        cols = row.find_all('td')
        if len(cols) >= 2:
            date = cols[0].text.strip()
            revenue = cols[1].text.strip().replace('$', '').replace(',', '')
            data.append({"Date": date, "Revenue": revenue})


tesla_revenue = pd.DataFrame(data, columns=["Date", "Revenue"])

print(tesla_revenue.head())

#Execute the following line to remove the comma and dollar sign from the Revenue column.

tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',|\$',"")
#Execute the following lines to remove an null or empty strings in the Revenue column.
tesla_revenue.dropna(inplace=True)
#Display the last 5 row of the tesla_revenue dataframe using the tail function. Take a screenshot of the results.
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]
 #### Use yfinance to Extract Stock Data####
##Using the Ticker function enter the ticker symbol of the stock we want to extract 
##data on to create a ticker object. The stock is GameStop and its ticker symbol is GME.
GameStop_ticker = yf.Ticker("GME")
GameStop_ticker
##Using the ticker object and the function history extract stock information and save it in a dataframe named gme_data. 
##Set the period parameter to "max" so we get information for the maximum amount of time.
gme_data = GameStop_ticker.history(period="max")
##Reset the index using the reset_index(inplace=True) function on the gme_data DataFrame and display the first five rows of the gme_data dataframe using the head function. 
##Take a screenshot of the results and code from the beginning of Question 3 to the results below.
gme_data.reset_index(inplace=True)
gme_data
###########Use Webscraping to Extract GME Revenue Data#################

url="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"
html_data_2 = requests.get(url).text
#Parse the html data using beautiful_soup using parser i.e html5lib or html.parser.
soup = BeautifulSoup(html_data_2,"html.parser")
##Using BeautifulSoup or the read_html function extract the table with GameStop Revenue and store it into a dataframe named gme_revenue. The dataframe should have columns Date and Revenue. 
##Make sure the comma and dollar sign is removed from the Revenue column.
GameStop_Revenue = pd.DataFrame(columns=["Date", "Revenue"])
data = []


tables = soup.find_all('table')


if len(tables) > 1:
    rows = tables[1].find_all('tr')
    for row in rows[1:]:  
        cols = row.find_all('td')
        if len(cols) >= 2:
            date = cols[0].text.strip()
            revenue = cols[1].text.strip().replace('$', '').replace(',', '')
            data.append({"Date": date, "Revenue": revenue})


GameStop_Revenue = pd.DataFrame(data, columns=["Date", "Revenue"])

print(GameStop_Revenue.head())

##Display the last five rows of the gme_revenue dataframe using the tail function. Take a screenshot of the results.
GameStop_Revenue.tail()
########Plot Tesla Stock Graph############

make_graph(tesla_data, tesla_revenue, 'Tesla')

make_graph(gme_data,GameStop_Revenue, 'GameStop')














