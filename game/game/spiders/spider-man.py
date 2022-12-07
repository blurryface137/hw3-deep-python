import scrapy
import re


class Steam_scrapy(scrapy.Spider):
    name = 'Steam'
    url = ['https://store.steampowered.com/search?term=adventure&ndl=1',
           'https://store.steampowered.com/search?term=adventure&page=2&ndl=1',

           'https://store.steampowered.com/search?term=open%20world&ndl=1',
           'https://store.steampowered.com/search?term=open%20world&page=2&ndl=1',

           'https://store.steampowered.com/search?term=story&ndl=1',
           'https://store.steampowered.com/search?term=story&page=2&ndl=1']

    def start_requests(self):
        for link in self.url:
            yield scrapy.Request(link, self.parse_games)

    def parse_games(self, response):
        urls = response.css('a.search_result_row::attr(href)').getall()
        for page in urls:
            yield scrapy.Request(page, self.parse_game)

    def parse_game(self, response):
        game_tags = response.css('div.glance_tags.popular_tags a::text').getall()
        for i in range(len(game_tags)):
            game_tags[i] = game_tags[i].strip()

        if response.css('span.platform_img.mac').get():
            flag1 = 'mac'
        else:
            flag1 = ''

        if response.css('span.platform_img.win').get():
            flag2 = 'win'
        else:
            flag2 = ''

        if response.css('span.platform_img.linux').get():
            flag3 = 'linux'
        else:
            flag3 = ''

        price = response.css('div.discount_final_price::text').get()
        if price == None:
            price = 'free'

        release = int(response.css('div.date::text').get()[-4:])
        if release > 2000:
            return {
                'name': response.css('div.apphub_AppName::text').get(),
                'category': response.css('div.blockbg a::text')[1:].getall(),
                'count_of_reviews': response.css('div.user_reviews_summary_bar span::text')[1].get(),
                'overall_score': response.css('span.game_review_summary::text').get(),
                'release': release,
                'developer': response.css('div.dev_row a::text').get(),
                'game_tag': game_tags,
                'price': price,
                'platform': flag1 + ' ' + flag2 + ' ' + flag3
            }
