import scrapy
from pprint import pprint

class UnivSpider(scrapy.Spider):
    name = "univ"

    def start_requests(self):
        urls = [
            'https://univ.cc/world.php'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for country in response.css("select option"):
            code = country.xpath("@value").extract()[0]
            if code == "world":
                continue
            country = country.xpath("text()").extract()[0]

            url = "https://univ.cc/search.php?start=1&dom=" + str(code)

            request = scrapy.Request(url=url, callback=self.parse_univ)
            request.meta['country'] = {
                'name' : country.encode('utf8'),
                'code' : code.encode('utf8'),
                'search_url' : url,
                'universities' : [],
            }
            yield request

    def parse_univ(self, response):
        for university in response.css("ol li a"):
            name = university.xpath("text()").extract()[0]
            url = university.xpath("@href").extract()[0]
            response.meta['country']['universities'].append({
                'name' : name.encode('utf8'),
                'url' : url.encode('utf8'),
            })

        link_url = response.xpath("//nav[@class='resultNavigation']/a[text()=' [>>Next]']/@href").extract()

        if len(link_url) > 0:
            self.logger.info("VISITING NEXT LINK : %s", str(link_url))
            request = response.follow("https://univ.cc/" + link_url[0], self.parse_univ)
            request.meta['country'] = response.meta['country']
            yield request
        else:
            yield response.meta['country']
