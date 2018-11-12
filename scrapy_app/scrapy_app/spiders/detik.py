# -*- coding: utf-8 -*-
import scrapy
import re
from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class NewsSpider(CrawlSpider):
	name = "detik"

	def __init__(self, *args, **kwargs):
		'''Inisialisasi Scraping
		self.url : Url yang digunaan memulai scraping
		domain : Domain dari pencarian. Jika domain detik.com, maka berita yang memiliki link republika.com tidak akan ditangkap
		'''
		self.url = kwargs.get('url')
		self.start_urls = [self.url]
		self.allowed_domains = ['detik.com']

	def parse(self, response):
		'''Memulai scraping
		urls : Mengambil semua URL Berita yang ada di list berita
		'''
		urls = response.xpath("//article/div/a/@href").extract()        
		for url in urls:
			print(url)
			url = response.urljoin(url)
			yield scrapy.Request(url=url, callback=self.parse_detail)

		# Menuju ke halaman selanjutnya, bila ada halaman selanjutnya.
		page_next =  response.xpath("//div[@class='center']/div/a/@href")[-1].extract()
		if page_next:
			page_next = response.urljoin(page_next)
			yield scrapy.Request(url=page_next, callback=self.parse)
	
	def parse_detail(self, response):
		# Format tanggal di dalam detik.com ialah : Kamis 01 Februari 2018,08:15 WIB
		# Coding dibawah ini digunakan untuk merubahnya menjadi standar datetime python 
		tanggalDetik = response.xpath("//div[@class='date']/text()").extract_first()
		BulanBahasa = {'Januari':1, 'Februari':2,'Maret':3,'April':4, 'Mei':5,'Juni':6,'Juli':7,'Agustus':8,'September':9,'Oktober':10,'November':11,'Desember':12}
		tanggal_split = tanggalDetik.split(' ')
		dd = int(tanggal_split[1])
		mm = BulanBahasa[tanggal_split[2]]
		yyyy = int(re.findall(r'\d+',tanggal_split[3])[0])
		jam_split =  re.findall(r'\d+',tanggal_split[4])
		hh = int(jam_split[0])
		hmm = int(jam_split[1])
		tanggal = datetime(yyyy,mm,dd,hh,hmm)
		
		# Mengirim data ke pipeline untuk disimpan
		i = {}
		i['breadcrumbs'] = response.xpath("//div[@class='breadcrumb']/a/text()").extract()
		i['penulis'] = response.xpath("//div[@class='author']/text()").extract_first()
		i['judul'] = response.xpath("normalize-space(//h1)").extract_first()
		i['berita'] = response.xpath("normalize-space(//div[@class='detail_text'])").extract_first()
		i['tag'] = response.xpath("//div[@class='detail_tag']/a/text()").extract()
		i['url'] = response.request.url
		i['website'] = 'detik'
		i['date'] = tanggal
		return i
