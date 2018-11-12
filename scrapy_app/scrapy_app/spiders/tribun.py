# -*- coding: utf-8 -*-
import scrapy
import re
from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class TribunSpider(CrawlSpider):
	name = 'tribun'

	def __init__(self, *args, **kwargs):
		'''Inisialisasi Scraping
		self.url : Url yang digunaan memulai scraping
		domain : Domain dari pencarian. Jika domain oekzone.com, maka berita yang memiliki link republika.com tidak akan ditangkap
		'''
		self.url = kwargs.get('url')
		self.start_urls = [self.url]
		self.allowed_domains = ['tribunnews.com']

	def parse(self, response):
		'''Memulai scraping
		urls : Mengambil semua URL Berita yang ada di list berita
		'''
		urls = response.xpath("//h3/a/@href").extract()       
		for url in urls:
			print(url)
			url = response.urljoin(url)
			yield scrapy.Request(url=url, callback=self.parse_detail)

		# Menuju ke halaman selanjutnya, bila ada halaman selanjutnya.
		page_next = response.xpath("//a[contains(text(),'Next')]/@href").extract_first()
		if page_next:
			page_next = response.urljoin(page_next)
			yield scrapy.Request(url=page_next, callback=self.parse)
	
	def parse_detail(self, response):
		# Format tanggal di dalam tribunnews.com ialah : Kamis, 1 Februari 2018 23:57 WIB
		# Coding dibawah ini digunakan untuk merubahnya menjadi standar datetime python
		tanggalTribun = response.xpath("//time/text()").extract_first()
		BulanBahasa = {'Januari':1, 'Februari':2,'Maret':3,'April':4, 'Mei':5,'Juni':6,'Juli':7,'Agustus':8,'September':9,'Oktober':10,'November':11,'Desember':12}
		tanggal_split = tanggalTribun.split(' ')
		dd = int(tanggal_split[1])
		mm = BulanBahasa[tanggal_split[2]]
		yyyy = int(tanggal_split[3])
		jam_split =  re.findall(r'\d+',tanggal_split[4])
		hh = int(jam_split[0])
		hmm = int(jam_split[1])
		tanggal = datetime(yyyy,mm,dd,hh,hmm)

		# Mengirim data ke pipeline untuk disimpan
		i = {}
		i['breadcrumbs'] = response.xpath("//h4/a/text()").extract()
		i['penulis'] = response.xpath("normalize-space(//div[@id='penulis'])").extract_first()
		i['judul'] = response.xpath("string(//h1)").extract_first()
		i['berita'] = response.xpath("//div/p//text()").extract()
		i['tag'] = response.xpath("//h5[@class='tagcloud3']/a/text()").extract()
		i['url'] = response.request.url
		i['website'] = 'tribun'
		i['date'] = tanggal
		return i

	# print("Start SPIDER")
	# name = 'detik'
	# allowed_domains = ['news.detik.com']
	# start_urls = ['https://news.detik.com/indeks/all/?date=02/28/2018'] #Ambil semua berita di hari tersebut
	# # start_urls = ['https://www.detik.com/search/searchall?query=banjir&sortby=time&fromdatex=01/02/2018&todatex=28/02/2018']
	# print("TO PARSE")
	# # def __init__(self, *args, **kwargs):
	#   # We are going to pass these args from our django view.
	#   # To make everything dynamic, we need to override them inside __init__ method
	#   # self.url = kwargs.get('url')
	#   # self.domain = kwargs.get('domain')
	#   # self.start_urls = [self.url]
	#   # self.allowed_domains = [self.domain]
	# def __init__(self, *args, **kwargs):
	#   NewsSpider.rules = [Rule(LinkExtractor(unique=True), callback='self.parse'),]

	# def parse(self, response):
	#   print("SEARCH LINK")
	#   urls = response.xpath("//article/div/a/@href").extract()        
	#   for url in urls:
	#       url = response.urljoin(url)
	#       yield scrapy.Request(url=url, callback=self.parse_detail)
		
	#   # follow pagination link
	#   # page_next =  response.xpath("//div[@class='center']/div/a/@href")[-1].extract()
	#   # page_next =   response.xpath("//a[@class = 'last']/@href").extract_first()
	#   # if page_next:
	#   #   page_next = response.urljoin(page_next)
	#   #   yield scrapy.Request(url=page_next, callback=self.parse)

	# def parse_detail(self,response):
	#   print("SCRAPEEE")
	#   x = {}
	#   x['breadcrumbs'] = response.xpath("//div[@class='breadcrumb']/a/text()").extract()
	#   x['tanggal'] = response.xpath("//div[@class='date']/text()").extract_first()
	#   x['penulis'] = response.xpath("//div[@class='author']/text()").extract_first()
	#   x['judul'] = response.xpath("//h1/text()").extract_first()
	#   x['berita'] = response.xpath("normalize-space(//div[@class='detail_text'])").extract_first()
	#   x['tag'] = response.xpath("//div[@class='detail_tag']/a/text()").extract()
	#   x['url'] = response.request.url
	#   return x

#if __name__ == '__main__':
#   scrap = NewsSpider("02/01/2018")