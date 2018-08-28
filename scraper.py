#!/usr/bin/env python3.7

import requests
import json
from lxml import html
import dateparser as dp
from datetime import timezone
import time
import re
from get_info import fetch_input

def page_pull():

    arg_list = fetch_input()
    query_url = arg_list[3]

    user_agent = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36'}
    #print(query_url)

    page = requests.get(query_url, headers=user_agent)
    #print(page.content)
    tree = html.fromstring(page.text)
    #print(tree)
    return tree, query_url


def date_parser(date_list):
    index = 0
    while index < len(date_list):
        hr_date = dp.parse(date_list[index])
        hr_date = int(time.mktime(hr_date.timetuple()))
        date_list[index] = hr_date
        index += 1
    return date_list

#def db_writer():


def file_write(data):
    with open('out.json', 'a') as write_file:
        json.dump(data, write_file, indent=4)
        write_file.write('\n')


def next_page_selector(tree,query_url):


    c_page_xpath =  '//div[@class="pagination"]/b'
    c_page = tree.xpath(c_page_xpath + '/text()')

    n_page_xpath = '//div[@class="pagination"]/a'


    n_page_link = tree.xpath(n_page_xpath + '/@href')

    index = 0
    while index < len(n_page_link):
        n_page_link[index] = query_url + re.sub(r"jobs.*&l=\w+", '' , n_page_link[index])
        index += 1
    #print('\n\n',n_page_link)

    n_page_num = tree.xpath(n_page_xpath + '/span[@class="pn"]/text()')

    n_page = n_page_num[0]
    #print(n_page, '\n')
    #print(n_page_link[0], '\n')
    print(f'Scraper is Now on page {c_page}. NEXT page is {n_page} with LINK: \n{n_page_link[0]}')
    return n_page_link

def newline_cleaner(job_list):
    index = 0
    while index < len(job_list):
        job_list[index] = job_list[index].strip('\n')
        if job_list[index] == '        ':
            job_list[index] = job_list[index].replace('        ','nothing')
        job_list[index] = job_list[index].strip(' ')
        index += 1
    return job_list


def extractor_jobDetails(tree):

    tree = page_pull()

    jobId_xpath = '//div[@data-tn-component="organicJob"]'

    jobId = tree.xpath(jobId_xpath + '/@id')
    jobLink = tree.xpath(jobId_xpath + '//a[@data-tn-element="jobTitle"]/@href')
    jobTitle = tree.xpath(jobId_xpath + '//a[@data-tn-element="jobTitle"]/@title')
    jobLocation = tree.xpath(jobId_xpath + '//span[@class="location"]/text()')
    jobCompany = newline_cleaner(tree.xpath(jobId_xpath + '//div//span[@class="company"]/text()'))
    jobDate = date_parser(tree.xpath(jobId_xpath + '//div[@class="result-link-bar"]/span[@class="date"]/text()'))
    jobDict = {
            'jobDetails':{
                'Id':'',
                'Date':'',
                'Link':'',
                'Title':'',
                'Location':'',
                'Company':'',
                }
            }

    index = 0

    while index < len(jobId):
        jobDict['jobDetails']['Id'] = jobId[index]
        jobDict['jobDetails']['Date'] = jobDate[index]
        jobDict['jobDetails']['Link'] = jobLink[index]
        jobDict['jobDetails']['Title'] = jobTitle[index]
        jobDict['jobDetails']['Location'] = jobLocation[index]
        jobDict['jobDetails']['Company'] = jobCompany[index]

        #write to file
        #print(jobDict,'\n')
        file_write(jobDict)
        index += 1


    #while index < len(jobAttrib):
    #    i

    #    hr_date = dp.parse(date_list[index])
    #    date_list[index] = hr_date
    #jobSponsored = has_sponsor(tree, jobId_xpath)
    #jobEasyapply = has_easyapply(tree, jobId_xpath)



if __name__ == '__main__':

    raw_page = page_pull()

    (tree,query_url) = raw_page

    next_page_selector(tree, query_url)
    extractor_jobDetails(tree)

