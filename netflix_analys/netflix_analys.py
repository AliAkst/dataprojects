#NETFLIXX DATA ANALYS
#gerrekli dosyalar
!pip install pandas
!pip install requests
!pip install bs4
!pip install html5lib
!pip install lxml
!pip install plotly
#step 1 import library
import pandas as pd
import requests
from bs4 import BeautifulSoup
#step 2 url degiskenine url yi atiyoruz
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/netflix_data_webpage.html"
#step 3 data degiskenine urlye gonderilen requestten gonderilen datayi atiyoruz
data  = requests.get(url).text
print(data)
#Parsing the data using the BeautifulSoup library
soup = BeautifulSoup(data, 'html.parser')
#Step 4: Identify the HTML tags
netflix_data = pd.DataFrame(columns=["Date", "Open", "High", "Low", "Close", "Volume"])

#Step 5: Use a BeautifulSoup method for extracting data

# First we isolate the body of the table which contains all the information
# Then we loop through each row and find all the column values for each row
for row in soup.find("tbody").find_all('tr'):
    col = row.find_all("td")
    date = col[0].text
    Open = col[1].text
    high = col[2].text
    low = col[3].text
    close = col[4].text
    adj_close = col[5].text
    volume = col[6].text

# Finally we append the data of each row to the table
netflix_data = pd.concat([netflix_data, pd.DataFrame(
{"Date": [date], "Open": [Open], "High": [high], "Low": [low], "Close": [close], "Adj Close": [adj_close],
         "Volume": [volume]})], ignore_index=True)
#Step 6: Print the extracted data
netflix_data.head()
