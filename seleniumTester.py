import time
from selenium import webdriver

driver = webdriver.Chrome('.')
driver.get('http://database.globalreporting.org/search');
driver.find_element_by_id("show-companies-toolbox").click()
driver.find_element_by_id('search-report-field').send_keys('toyota')
driver.find_element_by_id('go-report-search').click()
time.sleep(5) # Let the user actually see something!
driver.quit()