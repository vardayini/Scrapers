import scrapy
from scrapy.selector import HtmlXPathSelector


class CinemabotSpider(scrapy.Spider):
    name = 'cinemabot'
    allowed_domains = ['www.filmipop.com/ahmedabad/movie-showtimes']
    start_urls = ['https://www.filmipop.com/ahmedabad/movie-showtimes/']

    def parse(self, response):
        
        movie_names = response.css('#cityMovieShowTimes > div.ShowTimeView.w100p.fl.pdbtm4 > div > div > div > div> div > div.col-lg-9.col-md-9.col-sm-8.col-xs-12.pdbtm2 > div.movietitle.movietitleSEO > a > h1::text').extract()
        movie_rating =response.css('#cityMovieShowTimes > div.ShowTimeView.w100p.fl.pdbtm4 > div > div > div > div > div > div.col-lg-2.col-md-3.col-sm-4.col-xs-12 > div > div > div > div.pull-right.pos_rel > div > span::text').extract()

#        movie_perc = response.css('div.__percentage::text').extract()
       
        for item in zip(movie_names, movie_rating):
            scraped_info = {
                'name' : item[0],
                'rating' : item[1],
               
            }

            yield scraped_info

#//*[@id="now-showing"]/section[1]/div/div[2]/div[2]/div[1]/div/div/div[2]/div[4]/div/div[2]/div[1]/div[3] 

