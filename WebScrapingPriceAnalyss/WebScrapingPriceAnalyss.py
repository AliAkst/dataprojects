#####################################################
# Web Kazıma ile Rakip ve Fiyat Analizi
#####################################################

#####################################################
# İş Problemi
#####################################################

# Online kitap satışı yapan bir şirket, “Seyahat” ve “Kurgu Dışı” kategorilerinde
# az satış yaptığını tespit ediyor. Bu sebeple şirketin, rakip firmanın kazınması izin verilen
# https://books.toscrape.com/ adlı web sitesinden “Travel” ve “Nonfiction” kategorisindeki
# kitaplara ait bilgileri alıp, rakip ve fiyat analizi yapmaya ihtiyacı var. Şirket sizden
# bu kategorilerdeki her kitaba ait detay sayfasında bulunan bilgileri almanızı bekliyor.

#####################################################
# Proje Görevleri
#####################################################

# Projede İstenilen Akış
# ------------------------------------------
# "Travel" ve "Nonfiction" kategorilerine ait kitapların yer aldığı sayfa linkleri alınmalı.
# Sonrasında bir kategoriye ait tüm kitapların detay sayfalarının linkleri alındıktan sonra
# o kitapların detay bilgileri kazınmalı ve diğer kategoriye geçilmeli.

#####################################################################
# Görev 1: Tarayıcıyı Konfigüre Etme ve Başlatma
#####################################################################

import time
from bs4 import element
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# 1. Selenium'un Webdriver sınıfını kullanarak bir adet options adında ChromeOptions tanımlayınız.
options = webdriver.ChromeOptions()
# 2. Tanımladığınız options’a tam ekran özelliği ekleyiniz.
options.add_argument("--start-maximized")
# 3. Bir önceki adımlarda hazırladığınız options’ı da kullanarak bir adet driver adında Chrome tarayıcısı oluşturunuz.
driver = webdriver.Chrome(options)
driver.get("https://books.toscrape.com/")
time.sleep(2)

#####################################################################
# Görev 2: Ana Sayfanın İncelenmesi ve Kazınması
#####################################################################

# 1. Ana Sayfayı driver ile açınız ve inceleyiniz.
# 2. "Travel" ile "Nonfiction" kategori sayfalarının linklerini tutan elementleri tek seferde bulan XPath sorgusunu yazınız.
# 3. XPath sorgusu ile yakaladığınız elementleri driver'ı kullanarak bulunuz ve kategori detay linklerini kazıyınız.

elements = driver.find_elements(By.XPATH,"//a[contains(text(),'Travel') or contains(text(),'Nonfiction')]")

cat_urls = [element.get_attribute("href")for element in elements]
#####################################################################
# GÖREV 3: Kategori Sayfasının İncelenmesi ve Kazınması
#####################################################################
# 1. Herhangi bir detay sayfasına girip o sayfadaki kitapların detay linkini tutan elementleri yakalayan XPath sorgusunu yazınız.
driver.get(cat_urls[0])
time.sleep(2)
# 2. driver ile XPath sorgusunu kullanarak elementleri yakalayınız ve detay linklerini çıkarınız.
Book_elements = driver.find_elements(By.XPATH,"//div[@class='image_container']//a")
# 3. Sayfalandırma (Pagination) için butonlara tıklamak yerine sayfa linkini manipüle ediniz.
# İpucu: (Sayfa değiştikçe url'de ne değişiyor gözlemleyiniz)
# 4. Sayfalandırmanın sonuna geldiğinizi anlamak adına kategorinin 999. sayfasına giderek karşınıza çıkan sayfayı inceleyiniz.
#   İpucu: (..../category/books/nonfiction_13/page-999.html)
#   Dikkat: (..../category/books/travel_2/page-1.html ????????)
book_urls = [element.get_attribute("href") for element in Book_elements]
print(len(book_urls))
MAX_PAGINATION = 7
url =cat_urls[1]
book_urls = []
for i in range(1,MAX_PAGINATION):
    update_url = url if i == 1 else url.replace("index",f"page-{i}")
    driver.get(update_url)
    Book_elements = driver.find_elements(By.XPATH,"//div[@class='image_container']//a")
    if not Book_elements:
        break
    temp_urls = [element.get_attribute("href") for element in Book_elements]
    book_urls.extend(temp_urls)

print(len(book_urls))
# 5. Bir önceki adımdaki incelemenin sonucunda sayfalandırmada sonsuz döngüye girmemek adına kontrol kullanınız.
#   İpucu: (text'inde 404 içeren bir h1 var mı?) veya (if not product_list) ya da (len(product_list) <= 0)


#####################################################################
# GÖREV 4: Ürün Detay Sayfasının Kazınması
#####################################################################

# 1. Herhangi bir ürünün detay sayfasına girip class attribute'ı content olan div elementini yakalayınız.
driver.get(book_urls[0])
time.sleep(2)
content_div = driver.find_elements(By.XPATH,"//div[@class='content']")

#2. Yakaladığınız divin html'ini alınız ve inner_html adlı değişkene atayınız.

inner_html = content_div[0].get_attribute("innerHTML")

# 3. inner_html ile soup objesi oluşturunuz.
from bs4 import BeautifulSoup

soup = BeautifulSoup(inner_html,"html_parser")

# 4. Oluşturduğunuz soup objesi ile şu bilgileri kazıyınız:
# - Kitap Adı,
name_elem=soup.find("h1")
book_name = name_elem.text
#kitap fiyati
price_elem = soup.find("p",attrs={"class ": "price_color"})
book_price = price_elem.text
#kitap yildiz sayisi
import re
regex =re.compile('start-rating ')
star_elem = soup.find("p",attrs={"class":regex})
print(star_elem)
book_star_count = star_elem["class"][-1]
# - Kitap Açıklaması,
desc_elem = soup.find("div",attrs={"id":"product_description"}).find_next_sibling()
book_desc = desc_elem.text

# - Product Information Başlığı altında kalan tablodaki bilgiler.
product_info = {}
table_rows =soup.find("table").find_all("tr")
for row in table_rows:
    key = row.find("th").text
    value = row.find("td").text
    product_info[key]=value

#####################################################################
# GÖREV 5: Fonksiyonlaştırma ve Tüm Süreci Otomatize Etme
#####################################################################
# 1. İşlemleri fonksiyonlaştırınız. Örnek olarak: def get_product_detail(driver):   |    def get_category_detail_urls(driver)
def initialize_driver():
    '''initializes driver with maximized options'''
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options)
    return driver
def get_travel_and_nonfiction_category_urls(driver,url):
    '''Gets category urls from given homepage url'''
    driver.get(url)
    time.sleep(2)

    category_elements_xpath = "//a[contains(text(),'Travel')or contains(text(),'Nonfiction')]"


    category_elements= driver.find_elements(By.XPATH,category_elements_xpath)
    category_urls = [element.get_attribute["href"] for element in category_elements]

    return category_urls
def get_book_urls(driver,url):
    '''Gets book urls froom given category detail page url'''
    MAX_PAGINATION = 3


    book_urls = []
    book_elements_xpath = "//div[@class ='image_container']//a"
    for i in range(1,MAX_PAGINATION):
        updated_url = url if i == 1 else url.replace("index",f"page-{i}")
        driver.get(updated_url)
        time.sleep(2)
        book_elements = driver.find_elements(By.XPATH,book_elements_xpath)

def get_book_detail(driver,url):
    """Gets book data from given book detail page url"""
    driver.get(url)
    time.sleep(2)
    content_div  = driver.find_elements(By.XPATH,"//div[@class='content']")

    inner_html = content_div[0].get_attribute("innerHTML")

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(inner_html,"html.parser")

    name_elem = soup.find("h1")
    book_name = name_elem.text

    import re
    regex = re.compile('start-rating ')
    star_elem = soup.find("p", attrs={"class": regex})
    print(star_elem)
    book_star_count = star_elem["class"][-1]
    # - Kitap Açıklaması,
    desc_elem = soup.find("div", attrs={"id": "product_description"}).find_next_sibling()
    book_desc = desc_elem.text

    product_info = {}
    table_rows = soup.find("table").find_all("tr")
    for row in table_rows:
        key = row.find("th").text
        value = row.find("td").text
        product_info[key] = value

    return{'book name'book_name,'book price',book_price,'book star count',book_star_count,'book desc',book_desc,**product_info}

# 2. Süreci otomatize ederek, Travel ile Nonfiction kategorilerine ait tüm kitapların detaylarını alacak şekilde kodu düzenleyiniz.
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
Sleep_time =0.25

def main():
    BASE_URL ="https://books.toscrape.com/"
    driver = initialize_driver()
    category_urls=get_travel_and_nonfiction_category_urls(driver,BASE_URL)

    data = []
    for cat_url in category_urls:
        book_urls = get_book_urls(driver,cat_url)
        for book_url in book_urls:
            book_data = get_book_detail(driver,book_url)
            book_data["cat_url"] = cat_url
            data.append(book_data)

    len(data)

    import pandas as pd
    pd.set_option("display.max_columns",None)
    pd.set_option("display.max_colwidth, 40")
    pd.set_option("display.width",2000)
    df = pd.DataFrame(data)

    return  df

df = main()
print(df.head())
print(df.shape)