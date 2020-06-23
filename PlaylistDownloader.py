import selenium
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def getPlaylistLinks(url):
    sourceCode = requests.get(url).text
    soup = BeautifulSoup(sourceCode, 'html.parser')
    domain = 'https://www.youtube.com'
    links = []
    for link in soup.find_all("a", {"dir": "ltr"}):
        href = link.get('href')
        if href.startswith('/watch?'):
            links.append(domain + href)
    return links

def downloader(link, driver):
    driver.get('https://ytmp3.cc/en13/')
    inputElement = driver.find_element_by_id("input")
    inputElement.send_keys(link)

    inputElement.send_keys(Keys.ENTER)
    try:
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Download")))
        element.click()
        print('Downloading started!\n')
    except TimeoutException:
        print('Error occured!')
    
    
print("Made by: Nemanja Radoicic 2020")
print("Playlist needs to contain less than 100 videos, otherwise not all will be downloaded!\n")
link = input("Please input web address of playlist: ")
print('Loading videos...')
try:
    links = getPlaylistLinks(link)
    ukupno = len(links)
    print('Videos loaded: ' + str(ukupno))
    print('Starting downloader...')

    driver = webdriver.Chrome()

    trenutni = 1
    for link in links:
        print(link)
        print(str(trenutni) + '/' + str(ukupno))
        print('...')
        downloader(link, driver)
        trenutni += 1

    print('Downloading finnished!')
except:
    print("Error occured with playlist link! NOTE: Playlist needs to be public!")

