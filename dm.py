from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd


productNames=[] #商品名稱+品牌
prices = [] #特價價格
piclinks = [] #商品圖片連結
productLinks = []  #商品連結保存
brands=[] #品牌
pagelinks = []  #每一頁的網址
product_list =[]


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
            productLink = driver.find_element(By.XPATH, f'//*[@id="product-tiles"]/div[{i}]/div/a').get_attribute('href')
            productLinks.append(productLink)
        except:
            break


        #價格 ok
        price = driver.find_element(By.XPATH, f'//*[@id="product-tiles"]/div[{i}]/div/div[3]/div[2]/div/span[1]/span').get_attribute('textContent').replace('€','')
        prices.append(price)
        #商品名稱 OK
        productName = driver.find_element(By.XPATH, f'//*[@id="product-tiles"]/div[{i}]/div/div[3]/div[3]/a').get_attribute('textContent')
        productNames.append(productName)  
        #品牌 OK
        brand = driver.find_element(By.XPATH, f'//*[@id="product-tiles"]/div[{i}]/div/div[3]/div[3]/span').get_attribute('textContent')
        brands.append(brand)
        #商品圖片 OK
        piclink = driver.find_element(By.XPATH, f'//*[@id="product-tiles"]/div[{i}]/div/a/img').get_attribute('src')
        piclinks.append(piclink)
        # id
        # ids = [i.split(".html")[0][-13:] for i in productLinks]
        product_id = productLink.split(".html")[0][-13:]


        product_info = {
                'Store': "DM",
                'Product Name': productName,
                'Product Number': product_id,
                'Currency':"Eur",
                'Price':price,
                'Brand Name':brand,
                'Product URL':productLink,
                'Product Picture URL':piclink
            }


        product_list.append(product_info)
        
print(product_list)
driver.quit()


df = pd.DataFrame(product_list)
print(df.head())
df.to_csv('dm_fi.csv')

