import scrapy
import re
from urllib.parse import urljoin

def clean_score(score):
    score = int(score.replace('$','').replace(',',''))
    return score

class JeopardySpider(scrapy.Spider):
    name = 'jeop_data'

    custom_settings = {
        "DOWNLOAD_DELAY": 20,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 3,
        "HTTPCACHE_ENABLED": True
    }

    start_urls = [
            "http://www.j-archive.com/listseasons.php"
    ]

    def parse(self, response):
        # Extract the links to the seasons
        relevant_seasons = [str(x) for x in range(20,34)]
        for href in response.xpath(
            '//div[@id="content"]/table/tr/td/a/@href'
        ).extract():
            start_pos = href.find('=') + 1
            season = href[start_pos:]
            if season in relevant_seasons:
                yield scrapy.Request(
                url = urljoin("http://j-archive.com/",href),
                callback=self.parse_season,
                meta={'url':href,
                      'season':season}
                )

    def parse_season(self, response):
        season = response.request.meta['season']
        excludes = ['Tournament',
                    'Championship',
                    'Kids Week',
                    'Power Players',
                    'Celebrity',
                    'Battle of the Decades',
                    'Back to School']

        details = response.xpath(
            '//div[@id="content"]/table/tr/td[3]'
        ).extract()

        for i in range(0, len(details)):
            if not any(word in details[i] for word in excludes):
                episode = response.xpath('//div[@id="content"]/table/tr/td[1]/a/@href').extract()[i]
                yield scrapy.Request(
                    url=episode,
                    callback=self.parse_episode,
                    meta={'url':episode,
                          'season':season}
                    )

    def parse_episode(self, response):
        season = response.request.meta['season']
        title = response.xpath('/html/head/title/text()').extract()[0]
        id_start = title.find('#') + 1
        id_end = title.find(', ')
        game_id = title[id_start:id_end]
        date = title[-10:]

        names = response.xpath(
            '//div[@id="contestants"]/table/tr/td/p/a/text()'
            ).extract()

        urls = response.xpath(
            '//div[@id="contestants"]/table/tr/td/p/a/@href'
            ).extract()

        scores = response.xpath(
            '//div[@id="final_jeopardy_round"]/table[2]/tr/td/text()'
            ).extract()[3:6]

        DJ_scores = response.xpath(
            '//div[@id="double_jeopardy_round"]/table[2]/tr/td/text()'
            ).extract()[3:6]

        coryats = response.xpath(
            '//div[@id="final_jeopardy_round"]/table[3]/tr/td/text()'
            ).extract()[3:6]

        remarks = response.xpath(
            '//div[@id="final_jeopardy_round"]/table[3]/tr/td[@class="score_remarks"]'
            ).extract()

        for player in range(0,3):
            name = names[player]
            player_url = urls[player]
            player_start = player_url.find('=') + 1
            player_id = int(player_url[player_start:])
            podium = 2 - player

            score = clean_score(scores[podium])
            coryat = clean_score(coryats[podium])
            dj_score = clean_score(DJ_scores[podium])

            remark = remarks[podium]
            right = int(remark[26:(remark.find(" R"))])
            wrong = int(remark[(remark.find(",")+5):(remark.find(" W"))])
            DD_pos = [m.start() for m in re.finditer(' DD', remark)]
            DD = 0
            for pos in DD_pos:
                DD += int(remark[(pos-1)])

            yield {
                'season': season,
                'game_id': game_id,
                'date': date,
                'name': name,
                'player_id': player_id,
                'score': score,
                'coryat': coryat,
                'dj_score': dj_score,
                'right': right,
                'wrong': wrong,
                'DD': DD
            }
