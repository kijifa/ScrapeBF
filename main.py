# import libraries
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
import csv
import requests


def main():
    urlpage = "https://www.bezfrazi.cz"
    links_path = './data/links.csv'
    ignore_links = 'ignore_links.txt'
    gecko_path = r'./gecko/geckodriver.exe'
    max_page = 200

    print(urlpage)

    #driver = start_firefox(gecko_path)
    # get web page
    #driver.get(urlpage)

    # Load all pribehy
    #load_all_pribehy(driver, max_page)

    # Get_Links
    #links = get_links_list(driver)

    # Save links to csv file
    #ave_list_to_csv(links, links_path)

    # Close Firefox browser
    #close_firefox(driver)
    links = load_csv(links_path)
    ignore_list = load_csv(ignore_links)

    simp_links = simpler_list(links)
    simp_ignore = simpler_list(ignore_list)

    result_links = clean_list(simp_links, simp_ignore)
    print(result_links)
    print(len(result_links))



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


def get_links_list(driver):
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


def load_csv(file):
    with open(file, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)

    return data


def simpler_list(listin):
    result_list = []

    for item in listin:
        result_list.append(item[0])

    return result_list


def clean_list(listA, listB):
    result_list = set(listA) - set(listB)
    return result_list


def close_firefox(driver):
    # sleep for 30s
    time.sleep(5)
    # driver.quit()
    driver.quit()


def download_pages(links):

    return


if __name__ == "__main__":
    main()
