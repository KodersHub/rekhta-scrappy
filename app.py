
from flask import Flask, render_template, url_for, request, jsonify, make_response, flash, redirect
from flask_restful import Api, Resource
import time
import csv
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import requests
import re
from selenium import webdriver
from bs4 import BeautifulSoup

app = Flask(__name__)
api = Api(app)

options = Options()
options.add_argument('--headless')
options.add_argument('--profile-directory=Default') 
driver = webdriver.Chrome(options=options,executable_path='../chromedriver.exe')

# driver = webdriver.Chrome("chromedriver.exe")
# poet_link = "https://www.rekhta.org/poets/mirza-ghalib/ghazals"

def download_html(driver, poet_link):
    driver.get(poet_link)
        
    ### SCROLLING SHUGAL START HERE!
    SCROLL_PAUSE_TIME = 0.5

    ## Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        file = open("Ghalib.html", 'w')
        file.write(driver.page_source)
        file.close()


def writing_txt(driver):
    CHANGE_TIME = 1.0
        
    page = open('Ghalib.html', 'r')
    soup = BeautifulSoup(page, 'html.parser')
    page.close()
    info = soup.findAll('div', {'class': 'contentListItems nwPoetListBody'})

    links = []
    for each_business in info:
        # Your Fix here
        for a in each_business.find_all('a', href=True):
            links.append(a['href'])
            
    links_url = list(set(links))
    print("Total Ghazals: ", len(links_url))

    data = open("dataset.txt", 'w', encoding="utf-8")

    for i in range(len(links_url)):
        driver.get(links_url[i])
        ghazal_content = driver.find_elements_by_xpath('//div[@class="pMC"]')
        time.sleep(CHANGE_TIME)
        if not ghazal_content:
            print("Empty")
        else:
            data.write(ghazal_content[0].text)
            

    data.close()        
    driver.close()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        
        poet_link = request.form["url"]

        download_html(driver, poet_link)

        writing_txt(driver)
        
        with open('dataset.txt', 'r', encoding="utf-8") as f:
            b_lines = [ row for row in f ]
            
            return render_template('content.html', b_lines = b_lines)
                
    return render_template('index2.html')


 
if __name__ == "__main__":
    app.run(debug=True)



















