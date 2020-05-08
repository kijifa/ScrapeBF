# import libraries
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
import csv


def main():
    urlpage = "https://www.bezfrazi.cz"

    print(urlpage)

    driver = webdriver.Firefox(executable_path=r'./gecko/geckodriver.exe')
    # get web page
    driver.get(urlpage)
    # execute script to scroll down the page
    driver.find_element_by_link_text("Příběhy").click()
    time.sleep(10)
    # click Next button
    page = 1
    while page < 500:
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        try:
            driver.find_element_by_id("read-next-button").click()
            time.sleep(10)
            page += 1
        except:
            #page = 9999
            break

    elements = driver.find_elements_by_xpath("//a[@href]")
    links = []
    for elem in elements:
        links.append(elem.get_attribute("href"))

    with open('./data/links.csv', 'w', newline='') as file:
        for link in links:
            file.write(link)
            file.write('\n')

    # sleep for 30s
    time.sleep(5)
    # driver.quit()
    driver.quit()


if __name__ == "__main__":
    main()
