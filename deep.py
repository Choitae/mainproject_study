import scrapy


class DeepSpider(scrapy.Spider):
    name = 'deep'
    allowed_domains = ['https://www.folderstyle.com/shop/Pr_List.aspx?BrandCD=&CateIdx=1106&BrandCDs=&PageSize=20&CurrentPage=1&SortType=new&PriceCodes=&ColCodes=&SizeCodes=&CateIdxs=']
    start_urls = ['http://https://www.folderstyle.com/shop/Pr_List.aspx?BrandCD=&CateIdx=1106&BrandCDs=&PageSize=20&CurrentPage=1&SortType=new&PriceCodes=&ColCodes=&SizeCodes=&CateIdxs=/']


    def parse(self, response):
        pass


   print('a')