from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import csv


productNames=[] #商品名稱+品牌
prices = [] #特價價格
ids = [] #商品編號
piclinks = [] #商品圖片連結
productLinks = []  #商品連結保存
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

for i in range(0, total_pages):
    pagelinks.append(f'https://www.dm.de/ausverkauf?popularFacet0=Ausverkauf&isSellout0=true&purchasable0=true&pageSize0=10&sort0=editorial_relevance&currentPage0={i}')


# 獲取當前頁面的商品連結
for i in range(1,11):
    try:
        productLink = driver.find_element(By.XPATH, f'//*[@id="product-tiles"]/div[{i}]/div/a')
        productLinks.append(productLink.get_attribute('href'))
    except:
        break


    #進入連結 
for link in productLinks:
    driver.get(link)
    driver.implicitly_wait(10)

    # #商品圖片 --OK
piclink = driver.find_element(By.XPATH, '//*[@id="detail-image-container"]/div[2]/div/ol/li[1]/div/button/img')
piclinks.append(piclink.get_attribute('src')) 

#商品+品牌名稱 OK --
productName = driver.find_element(By.XPATH, '//*[@id="mainSectionContainer"]/div[2]/div[1]/div[1]/div[2]/div[1]/h1')
productName = productName.text
productNames.append(productName)


# products id --OK
id = driver.find_element(By.XPATH, '//*[@id="content-Produktbeschreibung"]/div/div/div[3]/div/div[2]')
ids.append(id.text)


#特價價格  --OK
price = driver.find_element(By.XPATH, '//*[@id="mainSectionContainer"]/div[2]/div[1]/div[1]/div[2]/div[5]/div[1]/div[1]/div[1]/div[1]/div/div/span[1]/span')
prices.append(price.text)
    

driver.quit()



for a,b,c,*d in ids,productNames,prices,piclinks:
    data.append({
            'Id': a,
            '商品名稱+品牌': b,
            '特價價格' : c,
            '圖片連結': d

    })



with open('dm.csv', 'w', newline='', encoding='utf-8-sig') as file:

    writer = csv.writer(file)
    for item in data:
        writer.writerow([item['Id'], item['商品名稱'], item['特價價格'], item['圖片連結']])

driver.quit()
