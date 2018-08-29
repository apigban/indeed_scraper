#!/usr/bin/env python3.7

import requests
import json
from lxml import html
import dateparser as dp
from datetime import timezone
import time
import re
import redis
import login_redis as lr
from get_info import fetch_input
import concurrent.futures

def page_pull():

    query_url = redis_session.lpop('page_url')

    arg_list = fetch_input()

    user_agent = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36'}

    page = requests.get(query_url, headers=user_agent)
    tree = html.fromstring(page.text)
    return tree, query_url


def date_parser(date_list):             #Exact dates after 1 month is not possible
    index = 0                           #indeed is not showing exact dates after 30 days
    while index < len(date_list):
        date_list[index] = date_list[index].replace('+','')  #strip symbols from dates
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


def newline_cleaner(job_list):
    index = 0
    while index < len(job_list):
        job_list[index] = job_list[index].strip('\n')
        if job_list[index] == '        ':
            job_list[index] = job_list[index].replace('        ','nothing')
        job_list[index] = job_list[index].strip(' ')
        index += 1
    return job_list


def extractor_jobDetails():

    (tree,query_url) = page_pull()

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
        file_write(jobDict)
        index += 1


    #while index < len(jobAttrib):
    #    i

    #    hr_date = dp.parse(date_list[index])
    #    date_list[index] = hr_date
    #jobSponsored = has_sponsor(tree, jobId_xpath)
    #jobEasyapply = has_easyapply(tree, jobId_xpath)


def login_redis():

    redis_retrieve = redis.StrictRedis(
            host = lr.login['ip'],
            port = lr.login['port'],
            password = lr.login['password'],
            db = lr.login['db']
            )
    print('<<Redis AUTH OK>>')
    return redis_retrieve



if __name__ == '__main__':

    redis_session = login_redis()

    (tree,query_url) = page_pull()
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        for url in redis_session.lrange('page_url', 0, -1):
            futures = [executor.submit(extractor_jobDetails)]
            print(futures)
