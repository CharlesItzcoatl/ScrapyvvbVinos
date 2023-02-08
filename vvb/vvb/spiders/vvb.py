import scrapy
import re

class Spidervvb(scrapy.Spider):
    name = 'vvb'
    start_urls = ['https://vvb.com.mx/wp/']
    custom_settings = {
        'FEED_URI': 'vvb.json', 
        'FEED_FORMAT': 'json',
        'FEED_EXPORT_ENCODING': 'utf-8',
        'ROBOTSTXT_OBEY': True,
        #'USER_AGENT': 'Chrome/104.0.5112.101',
    }

    def parse(self, response):
        countries = response.xpath('//ul[@class = "sub-menu"]/li/a/@href').getall()
        for country in countries:
            yield response.follow(country, callback=self.parse_vineyard)

    
    def parse_vineyard(self, response):
        vineyards = response.xpath('//a[contains(@class, "qodef-shortcode qodef-m")]/@href').getall()
        vineyards.pop()
        for vineyard in vineyards:
            yield response.follow(vineyard, callback=self.parse_products)

    
    def parse_products(self, response):
        products = response.xpath('//div[@class = "qodef-grid-inner clear"]//div[@class ="qodef-woo-product-inner"]/a/@href').getall()
        for product in products:
            yield response.follow(product, callback=self.parse_product, cb_kwargs = {'URL': product})


    def parse_product(self, response, **kwargs):
        url = kwargs['URL']
        value = []
        is_world = re.compile(r'^Nuevo|Viejo Mundo$')

        product = response.xpath('//h3[contains(@class, "product_title")]/text()').get()
        if(product.find('|') != -1):
            (vineyard, product_name) = product.split(' | ')
        else:
            vineyard = product
            product_name = product

        region = response.xpath('//span[@class = "posted_in"]/span[@class = "qodef-woo-meta-value"]/a/text()').getall()
        if len(region) < 2:
            country = 'Sin Categorizar'
            world = 'Sin Categorizar'
        elif not is_world.match(region[1]):
            world, country = region
        else:
            country, world = region

        value = response.xpath('//div[contains(@class, "woocommerce-product-details")]/p[1]/span/text()').get()
        if not value or value == 'N/A':
            value = response.xpath('//div[contains(@class, "woocommerce-product-details")]/p[1]/text()').get()

        yield {
            'Producto': product_name,
            'Bodega': vineyard,
            'País': country,
            'Mundo': world,
            'Tipo': value,
            'URL': url,
        }