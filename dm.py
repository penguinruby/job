from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import csv


productNames=[] #商品名稱+品牌
prices = [] #特價價格
piclinks = [] #商品圖片連結
productLinks = []  #商品連結保存
brands=[] #品牌
pagelinks = []  #每一頁的網址
data =[]



driver=webdriver.Chrome()
driver.get("https://www.dm.de/ausverkauf")
driver.implicitly_wait(10)
wait = WebDriverWait(driver, 10)



total_product= int(driver.find_element(By.XPATH, '//*[@id="mainSectionContainer"]/div[2]/div/div[2]/div/div/div[2]/span/b').text)

#下一頁 OK
count=0
total_pages= (total_product//10)+1

for i in range(0, total_pages+1):
    pagelinks.append(f'https://www.dm.de/ausverkauf?popularFacet0=Ausverkauf&isSellout0=true&purchasable0=true&pageSize0=10&sort0=editorial_relevance&currentPage0={i}')


for link in pagelinks:
    driver.get(link)
    driver.implicitly_wait(10)
    # 獲取當前頁面的商品連結 
    for i in range(1,11):
        try:
            productLink = driver.find_element(By.XPATH, f'//*[@id="product-tiles"]/div[{i}]/div/a')
            productLinks.append(productLink.get_attribute('href'))
        except:
            break
        #價格 ok
        price = driver.find_element(By.XPATH, f'//*[@id="product-tiles"]/div[{i}]/div/div[3]/div[2]/div/span[1]/span')
        prices.append(price.get_attribute('textContent'))
        #商品名稱 OK
        productName = driver.find_element(By.XPATH, f'//*[@id="product-tiles"]/div[{i}]/div/div[3]/div[3]/a')
        productNames.append(productName.get_attribute('textContent'))  
        #品牌 OK
        brand = driver.find_element(By.XPATH, f'//*[@id="product-tiles"]/div[{i}]/div/div[3]/div[3]/span')
        brands.append(brand.get_attribute('textContent'))
        #商品圖片 OK
        piclink = driver.find_element(By.XPATH, f'//*[@id="product-tiles"]/div[{i}]/div/a/img')
        piclinks.append(piclink.get_attribute('src'))
        # id
        ids = [i.split(".html")[0][-13:] for i in productLinks]



for a,b,c,d, *e in ids,brands,productNames,prices,piclinks:
    data.append({
            'Id': a,
            '商品品牌': b,
            '商品名稱': c,
            '特價價格' : d,
            '圖片連結': e

    })


with open('dm.csv', 'w', newline='', encoding='utf-8-sig') as file:

    writer = csv.writer(file)
    for item in data:
        writer.writerow([item['Id'], item['商品品牌'], item['商品名稱'], item['特價價格'],item['圖片連結']])

driver.quit()
