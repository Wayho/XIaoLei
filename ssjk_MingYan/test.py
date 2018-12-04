# coding: utf-8
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.wait import WebDriverWait

if __name__ == "__main__":
	options = Options()
	options.add_argument('-headless')  # 无头参数
	driver = Firefox( firefox_options=options)  # 配了环境变量第一个参数就可以省了，不然传绝对路径
	wait = WebDriverWait(driver, timeout=10)
	driver.get('https://www.baidu.com')
	print(driver.page_source)
	driver.quit()
