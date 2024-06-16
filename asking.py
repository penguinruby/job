''' 
Q1.測試太多次會被網站擋下(大約10來次以上，也有可能因為我每改依)。會跳到一個頁面去按"我不是機器人"。不幸的話，還會跳九宮格。請問有解決方式嗎？
Q2.用selenium自動化測試，為何還會被擋？所以用selenium也跟用request 是一樣的嗎
Q3.這個頁面的網址為https://www.mueller.de/sale/alle-produkte/，下一頁就是很規律的https://www.mueller.de/sale/alle-produkte/?p="數字"。
但是如果這次跑的時候全部只有28頁，把迴圈設定50頁的情況下，28頁之後全部都會出現在28頁。
也就是說，這樣28頁的東西就會抓好幾次。如果只設定28頁，但下次的特價頁面超過28頁的話，就又會抓不到。
不想用.click()下一頁的情況下，有可能解決這個問題嗎？


'''

from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.common.exceptions import NoSuchElementException
# from bs4 import BeautifulSoup

productNames=[] #商品名稱
prices = [] #特價價格
ids = [] #商品編號
piclinks = [] #商品圖片連結
productLinks = []  #商品連結保存
# pagelinks = []  #每一頁的網址


driver=webdriver.Chrome()
driver.get("https://www.mueller.de/sale/alle-produkte/")
driver.implicitly_wait(10)

#下一頁
# try:
#     for page in range(1,29):
#         links.append("https://www.mueller.de/sale/alle-produkte/?p="+str(page))
# except:
#     print("end")


for i in range (1,61):
#商品連結 OK
    productLink = driver.find_element(By.XPATH, '//*[@id="page"]/main/div[2]/div/div/div/div[2]/div[3]/div/div/a['+str(i)+']')
    productLinks.append(productLink.get_attribute('href'))

#進入連結 OK
for link in productLinks:
    driver.get(link)
    driver.implicitly_wait(10)

 #商品圖片 OK
    piclink = driver.find_element(By.XPATH, '//*[@id="page"]/main/div[1]/div/div[1]/div[1]/div[2]/div[1]/div/img')
    piclinks.append(piclink.get_attribute('src')) 

#商品名稱  OK
    productName = driver.find_element(By.XPATH, '//*[@id="page"]/main/div[1]/div/div[1]/div[2]/div[1]/h1')
    productNames.append(productName.text)


# products id OK
    id = driver.find_element(By.XPATH, '//*[@id="page"]/main/div[1]/div/div[1]/div[2]/div[1]/div[2]')
    ids.append(id.text)

#特價價格
    try:
        price = driver.find_element(By.XPATH, '//*[@id="page"]/main/div[1]/div/div[1]/div[2]/div[3]/div/div[1]/div[1]/span[3]')   #OK
        prices.append(price.text)
    except:
        price = driver.find_element(By.XPATH, '//*[@id="page"]/main/div[1]/div/div[1]/div[2]/div[3]/div/div[1]/div[1]/span[2]')   #OK
        prices.append(price.text)
    else:
        price = driver.find_element(By.XPATH, '//*[@id="page"]/main/div[1]/div/div[1]/div[2]/div[3]/div/div[1]/div/div/div[2]')  #ok
        prices.append(price.text)

driver.quit()

