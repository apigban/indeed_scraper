#!/usr/bin/env python3.7

import re
import redis
from scraper import page_pull


r = redis.Redis(
        host = '127.0.0.1',
        port = 6379,
        password = 'MerQuae1')

def next_page_selector(tree,query_url):



    c_page_xpath =  '//div[@class="pagination"]/b'
    c_page = tree.xpath(c_page_xpath + '/text()')

    n_page_xpath = '//div[@class="pagination"]/a[position()<last()]'

    n_page_links = [query_url]
    n_page_links_tree = tree.xpath(n_page_xpath + '/@href')

    index = 0
    while index < len(n_page_links_tree):
        n_page_links.append(query_url + re.sub(r"jobs.*&l=\w+", '' , n_page_links_tree[index]))
        index += 1
    print('\n\n', n_page_links)

    n_page_num = tree.xpath(n_page_xpath + '/span[@class="pn"]/text()')
    n_page = n_page_num[0]
    print(n_page, '\n')
    print(n_page_links_tree, '\n')
    #print(f'Scraper is Now on page {c_page}. NEXT page is {n_page} with LINK: \n{n_pag    e_link[0]}')
    return n_page_links




next_page_selector(*page_pull())

