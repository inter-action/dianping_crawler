from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = None
is_driver_closed = False


def get_driver():
    global driver
    if driver is not None and is_driver_closed != True:
        return driver

    print("create new driver")
    driver = webdriver.Chrome()

    return driver


def navi_to(url):
    get_driver().get(url)


def find_elements(sel):
    return driver.find_elements_by_css_selector(sel)


def find_element(sel):
    return driver.find_element_by_css_selector(sel)

def close():
    global driver
    global is_driver_closed
    if driver is not None and is_driver_closed != True:
        is_driver_closed = True
        driver.close()