import os
import sys
import threading
import googleapiclient.discovery
import json
from types import SimpleNamespace
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
linklistLock = threading.Lock()

def downloadTrack(link):
    global linklist
    global window
    link = "https://www.youtube.com/watch?v=" + link
    try:
        window.get("http://ytmp3.cc");
        window.find_element_by_id("input").send_keys(link)
        window.find_element_by_id("submit").click()
        while not window.find_element_by_xpath("/html/body/div[2]/div[1]/div[1]/div[3]/a[1]").is_displayed():
            sleep(1)
        window.find_element_by_xpath("/html/body/div[2]/div[1]/div[1]/div[3]/a[1]").click()
    except:
        print(link)

def threadDownloadList():
    global linklist
    while True:
        while len(linklist) == 0:
            sleep(1)
        downloadTrack(linklist[0])
        linklistLock.acquire()
        linklist.pop(0);
        linklistLock.release()

def readYTPlaylist(id):
    global linklist
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    api_service_name = "youtube"
    api_version = "v3"
    developer_key = "AIzaSyAxcDtfmVlZsa0QT-bKQ8Kct9gHuegKWpA"
    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey = developer_key)
    request = youtube.playlistItems().list(part="snippet", maxResults=1000, playlistId=id)
    response = request.execute()["items"]
    for i in range(0, len(response)):
        linklist.append(response[i]["snippet"]["resourceId"]["videoId"])
    print("Loaded YT playlist")

if len(sys.argv) == 2:
    with open(sys.argv[1], "r") as f:
        linklist = f.readlines()

downthrd = threading.Thread(target=threadDownloadList)
downthrd.start()

print("Linfinity Music\nType 'exit' anytime to quit!\n")

while True:
    newlink = input("Paste link: ")
    if newlink == "exit":
        os._exit(0)
    newlink = newlink.replace("http://", "").replace("https://", "").replace("www.", "").replace("youtube.com/", "")
    if newlink.startswith("playlist"):
        newlink = newlink.replace("playlist?list=", "")
        readYTPlaylist(newlink)
    elif newlink.startswith("watch"):
        newlink = newlink.replace("watch?v=", "")[0:11]
        linklist.append(newlink)
        print("Loaded video link")
