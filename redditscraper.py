import scrapy


class CinemabotSpider(scrapy.Spider):
    name = 'reddit'
    allowed_domains = ['www.reddit.com/r/gameofthrones']
    start_urls = ['http://www.reddit.com/r/gameofthrones/']

    def parse(self, response):
        names = response.css('.name.may-blank::text').extract()
        num_of_votes = response.css('.score.unvoted::text').extract()
        time= response.css('time::attr(name)').extract()
        num_of_comments = response.css('.comments::text').extract()
       
        for item in zip(names,num_of_votes,time,num_of_comments):
            scraped_info = {
                'name' : item[0],
                ‘vote’ : item[1],
                'created_at' : item[2],
                'num_of_comments' : item[3],
            }

            yield scraped_info
