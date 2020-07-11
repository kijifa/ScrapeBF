from bs4 import BeautifulSoup
from selenium import webdriver
from urllib import request
from urllib.request import urlopen
import csv
import logging
import time


def main():
    logging.basicConfig(filename='./log/loging.log', level=logging.DEBUG)

    urlpage = "https://www.bezfrazi.cz"
    links_path = './data/links.csv'
    ignore_links = 'ignore_links.txt'
    gecko_path = r'./gecko/geckodriver.exe'
    articles_folder = './data/articles/'
    max_page = 200

    logging.info('Start')
    driver = start_firefox(gecko_path)
    # get web page
    driver.get(urlpage)

    # Load all pribehy
    load_all_pribehy(driver, max_page)

    # Get_Links
    links = get_links_list(driver)

    # Save links to csv file
    save_list_to_csv(links, links_path)

    # Close Firefox browser
    close_firefox(driver)

    # Links loaded from csv file
    links = load_csv(links_path)

    # List links for ignore
    ignore_list = load_csv(ignore_links)

    # Simpler link. Destroy nested list
    simp_links = simpler_list(links)
    simp_ignore = simpler_list(ignore_list)

    # Final links list
    result_links = clean_list(simp_links, simp_ignore)
    #print(result_links)

    # Download files
    sample_links = ['https://www.bezfrazi.cz/nahradnik/', 'https://www.bezfrazi.cz/fotoalbum-v-zrcadle/']
    download_articles = download_pages(sample_links, articles_folder)


def start_firefox(gecko_path):
    """
    Start web browser
    :param gecko_path: path to gecko driver for web driver
    :return:
    """
    return webdriver.Firefox(executable_path=gecko_path)


def load_all_pribehy(driver, max_page):
    """
    Load pages with Pribehy, clicking to next button
    :param driver: web browser driver
    :param max_page: max number of clicking next button
    :return:
    """
    # execute script to scroll down the page
    driver.find_element_by_link_text("Příběhy").click()
    # wait for load all elements on page
    time.sleep(10)

    # init page for while
    page = 1
    # rolling over set number of pages
    while page < max_page:
        # Scroll to bottom page
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        # Try to find Next button. If not found break loop
        try:
            driver.find_element_by_id("read-next-button").click()
            time.sleep(10)
            page += 1
        except:
            break


def get_links_list(driver):
    """

    :param driver:
    :return:
    """
    elements = driver.find_elements_by_xpath("//a[@href]")
    links = []
    for elem in elements:
        links.append(elem.get_attribute("href"))

    return links


def save_list_to_csv(input_list, path):
    """
    Save list into csv file
    :param input_list: list you wanna save to csv
    :param path: path to csv file
    :return:
    """
    with open(path, 'w') as file:
        for item in input_list:
            file.write(item)
            file.write('\n')


def load_csv(file):
    """
    Loading csv file into variable
    :param file:
    :return:
    """
    with open(file, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)

    return data


def simpler_list(input_list):
    """
    Remove nested from list
    :param input_list: input nested list
    :return: list extracted from nested
    """
    result_list = []

    for item in input_list:
        result_list.append(item[0])

    return result_list


def clean_list(listA, listB):
    """
    Remove elements listB from listA
    :param listA: base list
    :param listB: list of elements should be remove from listA
    :return: elements from listA minus listB
    """
    result_list = set(listA) - set(listB)
    return result_list


def close_firefox(driver):
    """
    Closing web browser
    :param driver: web browser driver
    :return: empty return
    """
    # sleep for 30s
    time.sleep(5)
    # driver.quit()
    driver.quit()


def download_pages(links, articles_folder):
    """
    Process download articles page
    :param links: list of url links
    :param articles_folder: path to folder for articles save
    :return:
    """
    for link in links:
        print(link)
        # Save page to variable
        resp = request.urlopen(link).read().decode('utf8')
        # Convert html page to soup
        soup = BeautifulSoup(resp, 'html.parser')
        # Extract article title as article name
        article_name = extract_title(soup)
        # Save page locally
        save_article_page(link, article_name, articles_folder)
        time.sleep(10)
    return


def save_article_page(link, name, articles_folder):
    """
    Method saving html page localy
    :param link: link to page
    :param name: name of local file
    :return:
    """
    # Open and read url with article
    html = urlopen(link).read().decode('utf-8')

    # Save html file
    save_htm_file(html, articles_folder, name)

    return


def save_htm_file(content, folder, name):
    """
    Save html file to set folder
    :param content: content you wanna save
    :param folder: destination folder
    :param name: name of file output
    :return:
    """
    # Assemble file path
    file_path = folder + '/' + name + '.htm'

    # Create file and write content
    f = open(file_path, 'w', encoding='utf8')
    f.write(content)
    f.close()

    return


def extract_title(page):
    """
    Extracting title from downloaded page
    :param page: html code from webpage
    :return: clean title of article, no czech signs, no whitespace
    """
    # Extract title from html page
    title_str = page.find('h1', {"class": "post-title"}).text
    # Clean title
    clean_title = clean_czech_sign(title_str)
    return clean_title


def clean_czech_sign(text):
    """
    Cleaning czech sign in text
    :param text: text where you wanna replace czech signs
    :return: cleaned text
    """
    output = (
        text.replace(' ', '_')
        .replace('á', 'a')
        .replace('č', 'c')
        .replace('ď', 'd')
        .replace('é', 'e')
        .replace('ě', 'e')
        .replace('í', 'i')
        .replace('ň', 'n')
        .replace('ó', 'o')
        .replace('ř', 'r')
        .replace('š', 's')
        .replace('ť', 't')
        .replace('ú', 'u')
        .replace('ů', 'u')
        .replace('ž', 'z')
    )
    return output


if __name__ == "__main__":
    main()
