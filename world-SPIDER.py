# -*- coding: utf-8 -*-
import scrapy
import logging

class WorldSpider(scrapy.Spider):
    name = 'world'
    allowed_domains = ['www.worldometers.info']
    start_urls = ['https://www.worldometers.info/world-population/population-by-country/']

    def parse(self, response):
        countries= response.xpath("//td/a")
        for country in countries:
            country_name= country.xpath(".//text()").get()
            country_link= country.xpath(".//@href").get()

            #absolute_url=f"https://www.worldometers.info{country_link}"
            #absolute_url=response.urljoin(link)
            yield response.follow(url=country_link,callback=self.parse_country, meta={'country_name':country_name})

    
    def parse_country(self,response):
        country_name=response.request.meta['country_name']
        rows=response.xpath("//table[@class='table table-striped table-bordered table-hover table-condensed table-list']/tbody/tr")
        for row in rows:
            population=row.xpath(".//td[2]/strong/text()").get()
            yearly_change=row.xpath(".//td[3]/text()").get()
            median_age=row.xpath(".//td[6]/text()").get()
            fertility_rate=row.xpath(".//td[7]/text()").get()
            urban_population=row.xpath(".//td[10]/text()").get()


        yield{
            'country_name': country_name,
            'population': population,
            'yearly_change':yearly_change,
            'median_age':median_age,
            'fertility_rate':fertility_rate,
            'urban_population':urban_population




        }
