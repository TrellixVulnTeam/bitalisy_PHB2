# -*- coding: utf-8 -*-
import scrapy
import re
from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class KaskusSpider(CrawlSpider):
	name = 'kaskus'
	
	def __init__(self, *args, **kwargs):
		'''Inisialisasi Scraping
		self.url : Url yang digunaan memulai scraping
		domain : Domain dari pencarian. Jika domain kompas.com, maka berita yang memiliki link republika.com tidak akan ditangkap
		https://www.kaskus.co.id/search/forum?q=%27+keyword
		'''
		self.url = kwargs.get('url')
		self.start_urls = [self.url]
		self.allowed_domains = ['kaskus.com']

	def parse(self, response):
		'''Memulai scraping
		urls : Mengambil semua URL Berita yang ada di list berita
		'''
		urls = response.xpath("//table/tbody/tr/td/div/a/@href").extract()        
		for url in urls:
			print(url)
			yield scrapy.Request(url=url, callback=self.parse_detail)

		# Menuju ke halaman selanjutnya, bila ada halaman selanjutnya.
		page_next = ("//a[@data-original-title='Next Page']/@href").extract()
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
		i['post'] = response.xpath("//article[@class='Lh(1.5) Fz(14px)']").extract()
		i['time'] = response.xpath("//span/time/@datetime").extract()
		i['user'] = response.xpath("//div[@itemprop='name']/a/text()").extract()
		i['url'] = response.request.url
		i['website'] = 'kaskus'
		return i