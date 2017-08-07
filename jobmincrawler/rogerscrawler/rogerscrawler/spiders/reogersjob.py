import scrapy
from bs4 import BeautifulSoup
import psycopg2

class RogersJobSpider (scrapy.Spider):
    name = "reogerscrawler"
    # start_urls = [
    #     'https://jobs.rogers.com/search/?q=&locationsearch=',
    # ]
    url = 'https://jobs.rogers.com/search/?q=&sortColumn=referencedate&sortDirection=desc&startrow='
    start_urls =[] 
    increment = 0
    for i in range(14):
        new_url = url+str(increment)
        start_urls.append(new_url)
        increment += 25    
    def __init__(self, *args, **kwargs): 
        self.root_url = "https://jobs.rogers.com"
        self.next_page_xpath = '//*[@id="content"]/div/div[2]/div[2]/div/div/ul//li[@class="active"]//following-sibling::*/a/@href'

    def parse(self, response):
        all_jobs = response.xpath('//*[@id="searchresults"]/tbody/tr/td//a/@href')
        for job in all_jobs:
            yield response.follow(job, self.parse_job)


        

    def parse_job(self, response):
        def extract_with_xpath(query):
            return response.xpath(query).extract_first().strip()
        def province_parsing(address_string):
            provinces = ["AB","BC","MB","NB","NL","NS","NT","NU","ON","PE","QC","SK","YT"]
            province_initial = [i.strip()  for i in address_string.split(",") if i.strip() in provinces]
            if province_initial:
                return province_initial[0]
            else:
                return None      
        job_location_string = extract_with_xpath('//p[@class="jobLocation"]/span/text()')
        def job_description_parsing(response):
            soup = BeautifulSoup(response.body,"html.parser")   
            job = soup.find_all("div", class_="job") 
            job_description = str(job[0]).replace(u'\xa0', u' ').replace('\n', '')
            return job_description

        def insert_data(data_object):
            return
        yield {
            'title': extract_with_xpath('//div[@class="jobTitle"]/h1/text()'),
            'job_posted' : extract_with_xpath('//p[@class="jobDate"]/span/text()'),
            'job_location' : job_location_string,
            'province_name' : province_parsing(job_location_string),
            'job_detail' : job_description_parsing(response),
            'job_link' : response.url
        }
