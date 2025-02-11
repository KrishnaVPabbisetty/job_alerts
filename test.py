from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome()
driver.get("https://www.amazon.jobs")
print(driver.title)
driver.quit()
