#!/usr/bin/env python3.7

import argparse
#import requests


def url_creator(location, keyword):

    base_url = 'https://www.indeed.ae/jobs?'

    query_url = base_url + f'q={keyword}&l={location}'

   #print(query_url)
    return query_url

def fetch_input():
    """
    Gets parameters from command line arguments and
    passes it to indeed_scraper function in scraper file
    """

    arg_list = []

    parser = argparse.ArgumentParser(
            description = 'Script that gets job posts from indeed.com'
            )
    parser.add_argument(
            '--location',
            '-l',
            type = str,
            help = 'Specific Location of jobs to be fetched',
            required = True)
    parser.add_argument(
            '--keywords',
            '-kw',
            type = str,
            help = 'Job keywords',
            required = True,
            default = '')
    parser.add_argument(
            '--pages',
            '-p',
            type = str,
            help = 'Number of pages to scrape. Defaults to all',
            required = False,
            default = 'all')

    args = parser.parse_args()
    query_url = url_creator(args.location, args.keywords)

    args = parser.parse_args()
    arg_list.append(args.location)
    arg_list.append(args.keywords)
    arg_list.append(args.pages)
    arg_list.append(query_url)

    #print(arg_list)
    return arg_list

#fetch_input()


if __name__ == 'main':
    fetch_input()
