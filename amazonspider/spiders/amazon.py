# -*- coding: utf-8 -*-
import scrapy
import requests
import random
from lxml import etree
from ..settings import USER_AGENT
from ..items import AmazonspiderItem

class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    allowed_domains = ['amazon.cn']
    start_urls = ['http://amazon.cn/gp/site-directory']

    def parse(self, response):
        all_list = response.xpath("//div[contains(@class,'a-row')][position()>=3]")

        for tem_list in all_list:
            super_father_list = tem_list.xpath("./div[contains(@class, 'a-spacing-extra-large')]")
            sf_tmp = super_father_list.xpath('./span/a/text()').getall()
            super_father = '、'.join(sf_tmp)
            print(super_father)
            grandfather_list = tem_list.xpath(".//div[contains(@class, 'a-spacing-small')]")
            for gf in grandfather_list:
                grandfather = gf.xpath("./span/a/text()").get()
                print(grandfather)
                father_list = gf.xpath("./div[contains(@class, 'a-row')]//li")
                print('*'*100)
                for f in father_list:
                    father = f.xpath("./span/span/a/text()").get()
                    father_url = f.xpath("./span/span/a/@href").get()
                    father_url = response.urljoin(father_url)
                    print(father)
                    yield scrapy.Request(url=father_url, callback=self.goods_get, meta={'sf': super_father, 'gf': grandfather, 'f': father, })
        url = response.xpath("//span[contains(@class, 'pagnRA')]/a/@href").get()
        next_url = response.urljoin(url)
        if next_url:
            yield scrapy.Request(url=next_url, callback=self.parse)


    def goods_get(self, response):
        item_list = response.xpath('//ul[contains(@class, "s-result-list")]/li')

        for i in item_list:
            title = i.xpath('.//div[contains(@class, "a-spacing-mini")]/a/@title').get()
            price = i.xpath(".//span[contains(@class, 'a-size-base')]/text()").get()
            sum_rating = i.xpath(".//div[contains(@class, 'a-spacing-top-mini')]/a/text()").get()
            avg_rating = i.xpath(".//div[contains(@class, 'a-spacing-top-mini')]/span//span[contains(@class, 'a-icon-alt')]/text()")
            if avg_rating:
                avg_rating = avg_rating.get().split(' ')[1]
            else:
                avg_rating = 0

            item_id = i.xpath(".//div[contains(@class, 'a-spacing-top-mini')]/span/@name").get()
            url = 'https://www.amazon.cn/review/widgets/average-customer-review/popover/ref=acr_search__popover?'
            parms = {
                'ie': 'UTF8',
                'asin': item_id,
                'contextId': 'search',
                'ref': 'acr_search__popover'
            }
            user_agent = random.choice(USER_AGENT)
            headers = {
                'USER_AGENT': user_agent
            }
            re = requests.get(url=url, params=parms, headers=headers)
            # print(dir(re))
            # print('#'*100)
            # print(re.url)
            # print(re.text)
            html = etree.HTML(re.text)
            stars_tmp = html.xpath("//tr/td[3]")
            stars_list = []
            for tmp in stars_tmp:
                star_tmp = tmp.xpath(".//span[2]/text()")
                if star_tmp:
                    stars_list.append(star_tmp[0].strip())
                else:
                    stars_list.append(0)
            item = AmazonspiderItem(super_father=response.meta['sf'], grandfather=response.meta['gf'], father=response.meta['f'], title=title, price=price, sum_rating=sum_rating, avg_rating=avg_rating, ratings=stars_list)

            # print(title, price, sum_rating, avg_rating, item_id, stars_list)
            yield item

