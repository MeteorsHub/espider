from selenium import webdriver

url = 'https://500px.com/photo/80626185/refreshments-by-tim-santasombat'

cap = {}
cap['phantomjs.page.settings.resourceTimeout'] = 10000
cap['phantomjs.page.settings.loadImages'] = False
cap['phantomjs.page.settings.userAgent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'
driver = webdriver.PhantomJS(desired_capabilities=cap)
driver.get(url)
data = driver.page_source.encode('utf8')

with open('data.txt', 'w+', encoding = 'utf8') as f:
    f.write(data.decode('utf8'))