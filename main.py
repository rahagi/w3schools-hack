#!/usr/bin/env python3

from bs4 import BeautifulSoup
from urllib.request import urlopen
from FileWriter import mkdir, write, cd

PARENT_URL = 'https://w3schools.com/'
CHILD = ['html', 'css', 'js']

def get_navbar_links(child_url):
    w3_soup = BeautifulSoup(urlopen(PARENT_URL + child_url), 'html.parser')
    navbar_soup = BeautifulSoup(w3_soup.find(id="leftmenuinnerinner").encode('utf-8'), 'html.parser')
    url_list = []    

    for link in navbar_soup.find_all('a'):
        url_list.append(PARENT_URL + child_url + "/" + link.get('href'))

    return url_list

def get_editor_links(soup, child_url):
    links =[]
    for example in soup.find_all(class_="w3-example"):
        example_soup = BeautifulSoup(example.encode('utf-8'), 'html.parser')
        for link in example_soup.find_all('a'):
            links.append(PARENT_URL + child_url + "/" + link.get('href'))

    return links
def get_editor_soup(url):
    soup = BeautifulSoup(urlopen(url), 'html.parser')

    return soup.textarea.children

def get_code(editor_soup):
    code = ""
    for child in editor_soup:
        code += child.encode('utf-8').decode('utf-8')

    return code[4:]

def get_soup(url):
    return BeautifulSoup(urlopen(url), 'html.parser')

def prep_dir():
    for dir in CHILD:
        mkdir(dir)
    pass

if __name__ == '__main__':
    prep_dir()

    for mode in CHILD:
        navbar_list_links = get_navbar_links(mode)
        cd(mode)
        for link in navbar_list_links:
            print("downloading {}....".format(link))
            soup = get_soup(link)
            dirname = soup.title.get_text()
            editor_links = get_editor_links(soup, mode)
            i = 1
            for editor_link in editor_links:
                editor_soup = get_editor_soup(editor_link)
                code = get_code(editor_soup)
                write(dirname, str(i)+".html", code)              #end me
                i += 1
        cd('..')
