# -*- coding: utf-8 -*-
import scrapy
import re
from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class SindoSpider(CrawlSpider):
	name = 'sindo'

	def __init__(self, *args, **kwargs):
		'''Inisialisasi Scraping
		self.url : Url yang digunaan memulai scraping
		domain : Domain dari pencarian. Jika domain oekzone.com, maka berita yang memiliki link republika.com tidak akan ditangkap
		'''
		self.url = kwargs.get('url')
		self.start_urls = [self.url]
		self.allowed_domains = ['sindonews.com']

	def parse(self, response):
		'''Memulai scraping
		urls : Mengambil semua URL Berita yang ada di list berita
		'''
		urls = response.xpath("//div[@class='indeks-title']/a/@href").extract()        
		for url in urls:
			print(url)
			url = response.urljoin(url)
			yield scrapy.Request(url=url, callback=self.parse_detail)

		# Menuju ke halaman selanjutnya, bila ada halaman selanjutnya.
		page_next = response.xpath("//a[@rel='next']/@href").extract_first()
		if page_next:
			page_next = response.urljoin(page_next)
			yield scrapy.Request(url=page_next, callback=self.parse)
	
	def parse_detail(self, response):
		# Format tanggal di dalam sindo.com ialah : Rabu, 14 Februari 2018 - 17:09 WIB
		# Coding dibawah ini digunakan untuk merubahnya menjadi standar datetime python
		tanggalSindo = response.xpath("//time/text()").extract_first()
		BulanBahasa = {'Januari':1, 'Februari':2,'Maret':3,'April':4, 'Mei':5,'Juni':6,'Juli':7,'Agustus':8,'September':9,'Oktober':10,'November':11,'Desember':12}
		tanggal_split = tanggalSindo.split(' ')
		dd = int(tanggal_split[1])
		mm = BulanBahasa[tanggal_split[2]]
		yyyy = int(tanggal_split[3])
		jam_split =  re.findall(r'\d+',tanggal_split[5])
		hh = int(jam_split[0])
		hmm = int(jam_split[1])
		tanggal = datetime(yyyy,mm,dd,hh,hmm)

		# Mengirim data ke pipeline untuk disimpan
		i = {}
		i['breadcrumbs'] = response.xpath("//ul[@class='breadcrumb']//span/text()").extract()
		i['penulis'] = response.xpath("string(//p[@class='author'])").extract_first()
		i['judul'] = response.xpath("//h1/text()").extract_first()
		i['berita'] = response.xpath("string(//div[@id='content'])").extract_first()
		i['tag'] = response.xpath("//div[@class='tag-list']//a/text()").extract()
		i['url'] = response.request.url
		i['website'] = 'sindo'
		i['date'] = tanggal
		return i