#!/usr/bin/env python3.7

import re
import redis
import login_redis as lr
from get_info import fetch_input
import requests
from lxml import html


redis_dump = redis.StrictRedis(
        host = lr.login['ip'],
        port = lr.login['port'],
        password = lr.login['password'],
        db = lr.login['db']
        )


def create_queryURL():

    arg_list = fetch_input()
    query_url = arg_list[3]

    #user_agent = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KH    TML, like Gecko) Chrome/67.0.3396.79 Safari/537.36'}
    #print(query_url)

    #page = requests.get(query_url, headers=user_agent)
    #print(page.content)
    #tree = html.fromstring(page.text)
    #print(tree)
    return query_url


def next_page_linkGenerator(query_url):
    dec = []
    for item in range(0, 1000, 10):
        dec.append(str(item))

    page_links = [query_url]
    index = 1
    while index < len(dec):
        page_links.append(query_url + '&start=' + dec[index])
        index += 1
    return page_links


if __name__ == '__main__':

    query_url = create_queryURL()

    page_urls = next_page_linkGenerator(query_url)

    redis_dump.rpush('page_url',*page_urls)
