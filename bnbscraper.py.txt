import scrapy
import json
from bnbscraper.items import BnbscraperItem
import logging

QUERY = 'Jaipur--India'

class BnbspiderSpider(scrapy.Spider):
    name = "bnbspider"
    # allowed_domains = ["airbnb.com"]
    start_urls = (
        'https://www.airbnb.com/s/' + QUERY,
    )

    def parse(self, response):
        last_pg_number = self.last_pg_in_search(self, response)
        if last_pg < 1:
            return
        else:
            pg_urls = [response.url + "?section_offset=" + str(pgNum)
                         for pgNum in range(last_pg)]
            for pg_url in pg_urls:
                yield scrapy.Request(pg_url,
                                     callback=self.parse_list_results_pg)

    def parse_list_results_pg(self, response):
        room_url_parts = set(response.xpath('//div/a[contains(@href,"rooms")]/@href').extract())
        for href in list(room_url_parts):
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.parse_list_contents)

    def parse_list_contents(self, response):
        item = BnbscraperItem()



        item['title']=response.xpath('//*[@id="summary"]/div[2]/div[1]/div[2]/div[1]/div[1]/div/div/div[1]/div[1]/div/span/text()').extract()
        item['room_type'] =response.xpath('//*[@id="summary"]/div[2]/div[1]/div[2]/div[1]/div[2]/div/div[2]/div/div[2]/span/text()').extract()
        item['price'] =response.xpath('//*[@id="room"]/div/div[4]/div[1]/div/div[2]/div/div[2]/div/div/div/div[3]/div/div/div/div[2]/div[1]/div[1]/div[1]/div/strong/text()').extract()
        item['bed_number'] =response.xpath('//*[@id="summary"]/div[2]/div[1]/div[2]/div/div[2]/div/div/div/div[2]/div[1]/div/div[2]/span/text()').extract()
        item['person_capacity']=response.xpath('//*[@id="summary"]/div[2]/div[1]/div[2]/div/div[2]/div/div/div/div[1]/div[1]/div/div[2]/span/text()').extract()
        item['rating']=response.xpath('//*[@id="reviews"]/div/div[1]/div[1]/div/div[1]/div/div/div/h4/div/div/div/@content').extract()
        item['rating_communication'] =response.xpath('//*[@id="reviews"]/div/div[2]/div[1]/div[1]/div/div[2]/div/div[2]/div/span/@aria-label').extract()
        item['rating_cleanliness']=response.xpath('//*[@id="reviews"]/div/div[2]/div[1]/div[1]/div/div[3]/div/div[2]/div/span/@aria-label').extract()
        item['rating_checkin'] =response.xpath('//*[@id="reviews"]/div/div[2]/div[1]/div[2]/div/div[2]/div/div[2]/div/span/@aria-label').extract()
        item['value_for_money'] =response.xpath('//*[@id="reviews"]/div/div[2]/div[1]/div[2]/div/div[3]/div/div[2]/div/span/@aria-label').extract()
        item['accuracy_rating'] =response.xpath('//*[@id="reviews"]/div/div[2]/div[1]/div[1]/div/div[1]/div/div[2]/div/span/@aria-label').extract()
        item['language']=response.xpath('//*[@id="host-profile"]/div/span/span[2]/text()').extract()
        item['rev_count']= response.xpath('//*[@id="reviews"]/div/div[1]/div[1]/div/div[1]/div/div/div/h4/span/span/text()').extract()
        item['location_rating']= response.xpath('//*[@id="reviews"]/div/div[2]/div[1]/div[2]/div/div[1]/div/div[2]/div/span/@aria-label').extract()
        item['baths']=response.xpath('//*[@id="summary"]/div[2]/div[1]/div[2]/div[1]/div[2]/div/div[4]/div/div[2]/span/text()').extract()
        item['room_num']=response.xpath('//*[@id="summary"]/div[2]/div[1]/div[2]/div[1]/div[2]/div/div[2]/div/div[2]/span/text()').extract()
        item['guests']=response.xpath('//*[@id="summary"]/div[2]/div[1]/div[2]/div[1]/div[2]/div/div[1]/div/div[2]/span/text()').extract()
        item['url'] = response.url
        yield item

    def last_pgnumer_in_search(self, response):
        try:  # to get the last pg number
            last_pg = int(response
                                   .xpath('//ul[@class="list-unstyled"]/li[last()-1]/a/@href')
                                   .extract()[0]
                                   .split('section_offset=')[1]
                                   )
            print(response.xpath('//ul[@class="list-unstyled"]/li[last()-1]/a/@href'))
            return last_pg

        except KeyError:# if there is no pg number
            reason = response.xpath('//p[@class="text-lead"]/text()').extract()
            if reason and ('find any results that matched your request' in reason[0]):
                logging.log(logging.DEBUG, 'No results' + response.url)
                return 0
            else:
                return 1
