import pandas as pd
import requests
from bs4 import BeautifulSoup


base_link = 'https://www.khuyut.com/'

def scraping_khuyut_links():

    subs_links = extract_main_subs_links(base_link)
    links_all= []


    for sub_link in subs_links:
        mask = check_if_empty_page(base_link + sub_link)
        if mask:
            links_per_sub = extract_sub_links(base_link +sub_link)
            links_all = links_all + links_per_sub
    
    return links_all

def extract_sub_links(sub_link):

    links_per_sub = []

    n_page = 1
    updated_link = sub_link + '?aa89d540_page=' + str(n_page)

    is_not_last_page = check_if_empty_page(updated_link)
    
    while is_not_last_page:
        links_per_page = extract_page_links(updated_link)
        links_per_sub = links_per_sub + links_per_page
        n_page += 1
        updated_link = sub_link + '?aa89d540_page=' + str(n_page)
        is_not_last_page = check_if_empty_page(updated_link)


    return links_per_sub


def extract_page_links(url):
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all('a', class_= 'titleblowpic catgrid w-inline-block')

    links_per_page = []
    for link in results:
        links_per_page.append(link.get('href'))
    
    return links_per_page



    


def extract_main_subs_links(base_link):
    response = requests.get(base_link)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all('a', class_= 'fullmenusublink')

    subs_links = []
    for link in results:
        subs_links.append(link.get('href'))
    subs_links = subs_links[:37]
    
    return subs_links


def check_if_empty_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all('div', class_= 'w-dyn-empty')
    return not len(results)









