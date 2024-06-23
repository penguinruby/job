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
product_list =[]




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
        brand=driver.find_element(By.XPATH, f'//*[@id="page"]/main/div[2]/div/div/div/div[1]/div/ul/li[2]/div/div/ul/li[{i}]/label/div[2]/span[1]').text
        brands.append(brand)
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
            productLink = driver.find_element(By.XPATH, f'//*[@id="page"]/main/div[2]/div/div/div/div[2]/div[3]/div/div/a[{i}]').get_attribute('href')
            productLinks.append(productLink)
        except:
            break

    #進入連結 OK
for link in productLinks:
    driver.get(link)
    driver.implicitly_wait(10)

    #特價價格 OK
    try:
        price = driver.find_element(By.XPATH, '//*[@id="page"]/main/div[1]/div/div[1]/div[2]/div[3]/div/div[1]/div[1]/span[3]').text.replace(' €','')
        prices.append(price)
    except:
        try:
            price = driver.find_element(By.XPATH, '//*[@id="page"]/main/div[1]/div/div[1]/div[2]/div[3]/div/div[1]/div[1]/span[2]').text.replace(' €','')
            prices.append(price)
        except:
            try:
                price = driver.find_element(By.XPATH, '//*[@id="page"]/main/div[1]/div/div[1]/div[2]/div[3]/div/div[1]/div/div/div[2]').text.replace(' €','')
                prices.append(price)
            except:
                prices.append("not catch")
    # products id OK
    id = driver.find_element(By.XPATH, '//*[@id="page"]/main/div[1]/div/div[1]/div[2]/div[1]/div[2]').text.replace('Art.Nr.','') 
    ids.append(id)

    # #商品圖片 OK
    piclink = driver.find_element(By.XPATH, '//*[@id="page"]/main/div[1]/div/div[1]/div[1]/div[2]/div[1]/div/img').get_attribute('src')
    piclinks.append(piclink) 

    #商品名稱  OK
    productName = driver.find_element(By.XPATH, '//*[@id="page"]/main/div[1]/div/div[1]/div[2]/div[1]/h1').text
    productNames.append(productName)



# 遍歷每個商品名稱  OK
    matched_brand = "Unknown"
    for word in productName.split(" "):
        for brand in brandslowers:
            if brand in word.lower():
                matched_brand = brand
                break
        if matched_brand != "Unknown":
            break

    productsbrand.append(matched_brand)

    product_info = {
            'Store': "Muller",
            'Product Name': productName,
            'Product Number': id,
            'Currency':"EUR",
            'Price':price,
            'Brand Name':matched_brand,
            'Product URL':link,
            'Product Picture URL':piclink
        }


    product_list.append(product_info)
print(product_list)
driver.quit()


df = pd.DataFrame(product_list)
print(df.head())
df.to_csv('muller.csv')
