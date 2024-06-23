from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import csv


productNames=[] #商品名稱
prices = [] #特價價格
ids = [] #商品編號
piclinks = [] #商品圖片連結
productLinks = []  #商品連結保存
pagelinks = []  #每一頁的網址
brands=[] #全品牌蒐集
productsbrand=[] #商品品牌蒐集
brandslowers=[] #品牌大小寫轉換
data =[]




driver=webdriver.Chrome()
driver.get("https://www.mueller.de/sale/alle-produkte/")
driver.implicitly_wait(10)
wait = WebDriverWait(driver, 10)

#下一頁蒐集 OK
total_pages =int(driver.find_element(By.XPATH, '//*[@id="page"]/main/div[2]/div/div/div/div[2]/div[3]/div/nav/div/button[4]/span').text)
for i in range(1, total_pages):
    pagelinks.append(f'https://www.mueller.de/sale/alle-produkte/?p={i}')



#品牌蒐集 OK
for i in range(1,334):
    try:
        brand=driver.find_element(By.XPATH, f'//*[@id="page"]/main/div[2]/div/div/div/div[1]/div/ul/li[2]/div/div/ul/li[{i}]/label/div[2]/span[1]')
        brands.append(brand.text)
    except:
        break

        
for i in brands:  #品牌大小寫轉換以利配對 OK
    brandlower= i.lower()
    brandslowers.append(brandlower)


for link in pagelinks:
    driver.get(link)
    driver.implicitly_wait(10)
    # 獲取當前頁面的商品連結 OK
    for i in range(1, 61):  
        try:
            productLink = driver.find_element(By.XPATH, f'//*[@id="page"]/main/div[2]/div/div/div/div[2]/div[3]/div/div/a[{i}]')
            productLinks.append(productLink.get_attribute('href'))
        except:
            break

    #進入連結 OK
for link in productLinks:
    driver.get(link)
    driver.implicitly_wait(10)

    # #商品圖片 OK
    piclink = driver.find_element(By.XPATH, '//*[@id="page"]/main/div[1]/div/div[1]/div[1]/div[2]/div[1]/div/img')
    piclinks.append(piclink.get_attribute('src')) 

    #商品名稱  OK
    productName = driver.find_element(By.XPATH, '//*[@id="page"]/main/div[1]/div/div[1]/div[2]/div[1]/h1')
    productName = productName.text
    productNames.append(productName)

    for j in productNames:
        j= j.split(" ")


# 遍歷每個商品名稱  OK
    for product in j:
        matched = False
        for brand in brandslowers:
            if brand in product.lower():
                productsbrand.append(brand)
                matched = True
                break


    # products id OK
    id = driver.find_element(By.XPATH, '//*[@id="page"]/main/div[1]/div/div[1]/div[2]/div[1]/div[2]')
    ids.append(id.text)


#特價價格 OK
    try:
        price = driver.find_element(By.XPATH, '//*[@id="page"]/main/div[1]/div/div[1]/div[2]/div[3]/div/div[1]/div[1]/span[3]')
        prices.append(price.text)
    except:
        try:
            price = driver.find_element(By.XPATH, '//*[@id="page"]/main/div[1]/div/div[1]/div[2]/div[3]/div/div[1]/div[1]/span[2]')
            prices.append(price.text)
        except:
            try:
                price = driver.find_element(By.XPATH, '//*[@id="page"]/main/div[1]/div/div[1]/div[2]/div[3]/div/div[1]/div/div/div[2]')
                prices.append(price.text)
            except:
                prices.append("not catch")



for a,b,c,d,*e in ids,productNames,productsbrand,prices,piclinks:
    data.append({
            'Id': a,
            '商品名稱': b,
            '商品品牌' : c,
            '特價價格': d,
            '圖片連結': e

    })



with open('muller.csv', 'w', newline='', encoding='utf-8-sig') as file:

    writer = csv.writer(file)
    for item in data:
        writer.writerow([item['Id'], item['商品名稱'], item['商品品牌'], item['特價價格'],item["圖片連結"]])

driver.quit()
