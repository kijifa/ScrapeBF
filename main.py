# import libraries
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
import csv


def main():
    urlpage = "https://www.bezfrazi.cz"
    links_path = './data/links.csv'
    gecko_path = r'./gecko/geckodriver.exe'
    max_page = 200

    print(urlpage)

    driver = start_firefox(gecko_path)
    # get web page
    driver.get(urlpage)

    # Load all pribehy
    load_all_pribehy(driver, max_page)

    # Get_Links
    links = get_links_from_pribehy(driver)

    # Save links to csv file
    save_list_to_csv(links, links_path)

    # Close Firefox browser
    close_firefox(driver)


def start_firefox(gecko_path):
    return webdriver.Firefox(executable_path=gecko_path)


def load_all_pribehy(driver, max_page):
    # execute script to scroll down the page
    driver.find_element_by_link_text("Příběhy").click()
    time.sleep(10)

    page = 1
    while page < max_page:
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        try:
            driver.find_element_by_id("read-next-button").click()
            time.sleep(10)
            page += 1
        except:
            # page = 9999
            break


def get_links_from_pribehy(driver, max_page):
    elements = driver.find_elements_by_xpath("//a[@href]")
    links = []
    for elem in elements:
        links.append(elem.get_attribute("href"))

    return links


def save_list_to_csv(list, path):
    with open(path, 'w') as file:
        for item in list:
            file.write(item)
            file.write('\n')


def close_firefox(driver):
    # sleep for 30s
    time.sleep(5)
    # driver.quit()
    driver.quit()


if __name__ == "__main__":
    main()
