#!/usr/bin/env python3

from bs4 import BeautifulSoup
from urllib.error import HTTPError
from urllib.request import urlopen
from FileWriter import mkdir, write, cd

PARENT_URL = 'https://w3schools.com'
CHILD = ['html', 'css', 'js']

def get_navbar_links(child_url):
    w3_soup = BeautifulSoup(get_html(PARENT_URL + "/" + child_url), 'html.parser')
    navbar_soup = BeautifulSoup(w3_soup.find(id="leftmenuinnerinner").encode('utf-8'), 'html.parser')
    url_list = []    

    for link in navbar_soup.find_all('a'):
        if '/' in link.get('href'):
            url_list.append(PARENT_URL + "/" + child_url + link.get('href'))
        else:
            url_list.append(PARENT_URL + "/" + child_url + "/" + link.get('href'))

    return url_list

def get_editor_links(soup, child_url):
    links =[]
    for example in soup.find_all(class_="w3-example"):
        example_soup = BeautifulSoup(example.encode('utf-8'), 'html.parser')
        for link in example_soup.find_all('a'):
            try:
                if 'tryit' in link.get('href'):
                    links.append(PARENT_URL + "/" + child_url + "/" + link.get('href'))
            except TypeError as err:
                continue

    return links
def get_editor_soup(url):
    return BeautifulSoup(get_html(url), 'html.parser').textarea.children

def get_code(editor_soup):
    code = ""
    for child in editor_soup:
        code += child.encode('utf-8').decode('utf-8')

    return code[5:-2]

def get_soup(url):
    return BeautifulSoup(get_html(url), 'html.parser')

def prep_dir():
    for dir in CHILD:
        mkdir(dir.upper())
    pass

def get_html(url):
    try:
        return urlopen(url)
    except HTTPError as err:
        return ''

if __name__ == '__main__':
    prep_dir()

    for mode in CHILD:
        navbar_list_links = get_navbar_links(mode)
        cd(mode.upper())
        for link in navbar_list_links:
            print("downloading {} ....".format(link))
            soup = get_soup(link)
            try:
                dirname = soup.title.get_text()
            except AttributeError as err:
                continue
            editor_links = get_editor_links(soup, mode)
            i = 1                                                 #end me
            for editor_link in editor_links:
                try:
                    editor_soup = get_editor_soup(editor_link)
                    code = get_code(editor_soup)
                    write(dirname, str(i)+".html", code)              #end me
                    i += 1                                            #end me
                except AttributeError as err:
                    continue
        cd('..')
    print("done.")