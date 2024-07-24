###########################
### Web Scraping mini project
##########################
from bs4 import BeautifulSoup # this module helps in web scrapping.
import requests  # this module helps us to download a web page
html="<!DOCTYPE html><html><head><title>Page Title</title></head><body><h3><b id='boldest'>Lebron James</b></h3><p> Salary: $ 92,000,000 </p><h3> Stephen Curry</h3><p> Salary: $85,000, 000 </p><h3> Kevin Durant </h3><p> Salary: $73,200, 000</p></body></html>"
soup = BeautifulSoup(html, 'html5lib')
##We can use the method prettify() to display the HTML in the nested structure:

print(soup.prettify())

tag_object=soup.title
print("tag object:",tag_object)
#we can see the tag type bs4.element.Tag
print("tag object type:",type(tag_object))

tag_object=soup.h3

tag_object

tag_child =tag_object.b

tag_child

parent_tag=tag_child.parent

parent_tag

tag_object

tag_object.parent

sibling_1=tag_object.next_sibling

sibling_1

sibling_2=sibling_1.next_sibling

sibling_2

##########
# Downloading And Scraping The Contents Of A Web Page
##########
url = "http://www.ibm.com"
data  = requests.get(url).text
soup = BeautifulSoup(data,"html5lib")  # create a soup object using the variable 'data'
##Scrape all links
for link in soup.find_all('a',href=True):  # in html anchor/link is represented by the tag <a>

    print(link.get('href'))

######Scrape all images Tags
for link in soup.find_all('img'):# in html image is represented by the tag <img>
    print(link)
    print(link.get('src'))

    ####Scrape data from HTML tables
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DA0321EN-SkillsNetwork/labs/datasets/HTMLColorCodes.html"

data  = requests.get(url).text
soup = BeautifulSoup(data,"html5lib")
table = soup.find('table')
#Get all rows from the table
for row in table.find_all('tr'): # in html table row is represented by the tag <tr>
    # Get all columns in each row.
    cols = row.find_all('td') # in html a column is represented by the tag <td>
    color_name = cols[2].string # store the value in column 3 as color_name
    color_code = cols[3].string # store the value in column 4 as color_code
    print("{}--->{}".format(color_name,color_code))
