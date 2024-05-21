import scrapy


class TesterHomeTopicsSpider(scrapy.Spider):
    name = 'excellent_topics'
    allowed_domains = ['testerhome.com']
    start_urls = ['https://testerhome.com/topics/excellent']

    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'output.json',
        'FEED_EXPORT_ENCODING': 'utf-8',
        'DOWNLOAD_DELAY': 1.0  # 设置每次请求之间的等待时间为1秒
    }

    def __init__(self):
        self.processed_titles = set()  # 初始化一个空集合来存储已处理的标题

    def start_requests(self):
        cookies = {
            '_ga': 'GA1.2.1537469966.1658815398',
            '_ga_WWKG56X3TC': 'GS1.2.1687495884.1.0.1687495884.0.0.0',
            'sensorsdata2015jssdkcross': '%7B%22%24device_id%22%3A%2218c38383d08df1-0b1cab94a01eb5-1b525634-1296000-18c38383d099a6%22%7D',
            'user_id': 'eyJfcmFpbHMiOnsibWVzc2FnZSI6Ik1qVXhOVE09IiwiZXhwIjpudWxsLCJwdXIiOiJjb29raWUudXNlcl9pZCJ9fQ%3D%3D--039a506d96cc499c26d9ff9cbc5dfd568fbec6bf',
            'Hm_lvt_2c94babfa1f440b1bbbd2dac38628bec': '1702461243,1703143202,1703492869',
            '_gid': 'GA1.2.753168001.11703492870',
            'Hm_lpvt_2c94babfa1f440b1bbbd2dac38628bec': '1703582870',
            '_homeland_session': 'KJXY51gMwIXtULa7%2BoKi8o9j0Poo7AVsrDWb1j0MwGt9vNwpnj4KZX9CYzuooxTwDIK5mE5uL%2FQlc4saLG41TRlMrp4o8J%2B0p9cnEE5impfB6MVV0WlAHnz3OnagsVTCMuC4Uu3gi6447c76SGEK4c72YMkXAgX4nAJLYLW0TZVipnEBEPnlsTq1qKqcCD6nuviCwCpBOJ12DRzkl3KVgiKJAsgvDkMA0bTsgp14RHP5hwtH4HoRyr%2FW6BvJrKQijQQQMXcO8XuSKq8riPK6sLRPCN3u8y7iLI2so1cVBhxSI2v%2BmE3NeBf4Z2ai2s58U7tew3pNl7TtMAz6Owh1z1eglR9F%2BhcpF9f33XJTRowZA3aYoODV1tECOsEuo4RMPaDgfjM85CKsgPRd4GV7JQmOcT7Lt%2BLcJPjkwNDYU2cC%2Fg6RR91lw--uwhlW6UCm9NJpu6v--rUQQQYGNrq36%2B6hC%2F7FquA%3D%3D'
        }
        for url in self.start_urls:
            yield scrapy.Request(url, cookies=cookies, callback=self.parse)

    def parse(self, response):
        # 提取文章链接
        articles = response.css('div.title.media-heading a::attr(href)').getall()
        for article in articles:
            full_article_url = "https://testerhome.com" + article
            yield scrapy.Request(full_article_url, callback=self.parse_article, meta={'full_article_url': full_article_url})

        # 遵循分页链接
        next_page = response.css('li.page-item.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_article(self, response):
        # Retrieve the full_article_url from the meta dictionary
        full_article_url = response.meta['full_article_url']
        # 解析具体文章页面
        for topic in response.xpath('//span[@class="title"]'):
            title = topic.xpath('.//text()').get().strip()
            if title not in self.processed_titles:
                self.processed_titles.add(title)
                content_selector = topic.xpath('following::div[@class="card-body markdown markdown-toc"][1]')
                content = content_selector.xpath('.//p//text()').getall()
                content = ' '.join(content).strip() + "\nFor details, please refer to {0}".format(full_article_url)
                yield {
                    'prompt_responses': [
                        {
                            'prompt': title,
                            'responses': [content]
                        }
                    ]
                }
