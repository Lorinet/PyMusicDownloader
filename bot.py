from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from time import sleep
from threading import Thread
from time import sleep


def createHackfreeFirefox():
    pf = webdriver.FirefoxProfile()
    pf.set_preference("dom.webdriver.enabled", False)
    pf.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0")
    pf.set_preference('useAutomationExtension', False)
    return webdriver.Firefox(pf)

window = createHackfreeFirefox()
window.maximize_window()
linklist = []

with open(sys.argv[1], "r") as f:
    linklist = f.readlines()

for i in range(0, len(linklist)):
    try:
        window.get("http://ytmp3.cc");
        window.find_element_by_id("input").send_keys(linklist[i])
        window.find_element_by_id("submit").click()
        while not window.find_element_by_xpath("/html/body/div[2]/div[1]/div[1]/div[3]/a[1]").is_displayed():
            sleep(1)
        window.find_element_by_xpath("/html/body/div[2]/div[1]/div[1]/div[3]/a[1]").click()
        sleep(2)
    except:
        print(linklist[i])

window.close()

