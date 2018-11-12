# -*- coding: utf-8 -*-
import scrapy
import re
from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class KompasSpider(CrawlSpider):
	name = 'kompas'
	
	def __init__(self, *args, **kwargs):
		'''Inisialisasi Scraping
		self.url : Url yang digunaan memulai scraping
		domain : Domain dari pencarian. Jika domain kompas.com, maka berita yang memiliki link republika.com tidak akan ditangkap
		'''
		self.url = kwargs.get('url')
		self.start_urls = [self.url]
		self.allowed_domains = ['kompas.com']

	def parse(self, response):
		'''Memulai scraping
		urls : Mengambil semua URL Berita yang ada di list berita
		'''
		urls = response.xpath("//h3/a/@href").extract()        
		for url in urls:
			print(url)
			yield scrapy.Request(url=url, callback=self.parse_detail)

		# Menuju ke halaman selanjutnya, bila ada halaman selanjutnya.
		page_next = response.xpath("//a[@rel='next']/@href").extract_first()
		if page_next:
			page_next = response.urljoin(page_next)
			yield scrapy.Request(url=page_next, callback=self.parse)
	
	def parse_detail(self, response):
		# Format tanggal di dalam kompas ialah : 01/02/2018 , 08:15 WIB
		# Coding dibawah ini digunakan untuk merubahnya menjadi standar datetime python
		tanggalKompas = response.xpath("substring(//div[@class='read__time']/text(),14,21)").extract_first()
		tanggal_split = re.findall(r'\d+',tanggalKompas)
		dd = int(tanggal_split[0])
		mm = int(tanggal_split[1])
		yyyy = int(tanggal_split[2])
		hh = int(tanggal_split[3])
		hmm = int(tanggal_split[4])
		tanggal = datetime(yyyy,mm,dd,hh,hmm)

		# Mengirim data ke pipeline untuk disimpan
		i = {}
		i['breadcrumbs'] = response.xpath("//a/span/text()").extract()
		i['penulis'] = response.xpath("//div[@class='read__author']/a/text()").extract_first()
		i['judul'] = response.xpath("normalize-space(//h1[@class='read__title'])").extract_first()
		i['berita'] = response.xpath("normalize-space(//div[@class='read__content'])").extract_first()
		i['tag'] = response.xpath("//li/a[@class='tag__article__link']/text()").extract()
		i['url'] = response.request.url
		i['website'] = 'kompas'
		i['date'] = tanggal
		return i