# -*- coding: utf-8 -*-
import scrapy
import re
from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class RepublikaSpider(CrawlSpider):
	name = 'republika'

	def __init__(self, *args, **kwargs):
		'''Inisialisasi Scraping
		self.url : Url yang digunaan memulai scraping
		domain : Domain dari pencarian. Jika domain oekzone.com, maka berita yang memiliki link republika.com tidak akan ditangkap
		'''
		self.url = kwargs.get('url')
		self.start_urls = [self.url]
		self.allowed_domains = ['republika.co.id']

	def parse(self, response):
		'''Memulai scraping
		urls : Mengambil semua URL Berita yang ada di list berita
		'''
		urls = response.xpath("//h2/a/@href").extract()        
		sum_urls = float(response.xpath("count(//h2/a/@href)").extract_first())
		for url in urls:
			print(url)
			url = response.urljoin(url)
			yield scrapy.Request(url=url, callback=self.parse_detail)

		# follow pagination link
		# NO NEED IN TESTING
		page_next = response.xpath("//div[@class='pagination']/section/nav/a/@href")[-1].extract()
		if sum_urls != 0 :
			page_next = response.urljoin(page_next)
			yield scrapy.Request(url=page_next, callback=self.parse)
		

	def parse_detail(self, response):
		# Format tanggal di dalam republika.com ialah : Kamis 01 February 2018 23:52 WIB
		# Coding dibawah ini digunakan untuk merubahnya menjadi standar datetime python
		tanggalRepublika = response.xpath("normalize-space(//div[@class='date_detail']//p)").extract_first()
		BulanBahasa = {'January':1, 'February':2,'March':3,'April':4, 'May':5,'June':6,'July':7,'August':8,'September':9,'October':10,'November':11,'December':12, 'Januari':1, 'Februari':2,'Maret':3,'Mei':5,'Juni':6,'Juli':7,'Agustus':8,'Oktober':10,'Desember':12}
		tanggal_split = tanggalRepublika.split(' ')
		dd = int(tanggal_split[1])
		mm = BulanBahasa[tanggal_split[2]]
		yyyy = int(tanggal_split[3])
		jam_split =  re.findall(r'\d+',tanggal_split[4])
		hh = int(jam_split[0])
		hmm = int(jam_split[1])
		tanggal = datetime(yyyy,mm,dd,hh,hmm)

		# Mengirim data ke pipeline untuk disimpan
		i = {}
		i['breadcrumbs'] = response.xpath("normalize-space(//div[@class='breadcome'])").extract()
		i['penulis'] = response.xpath("normalize-space(//div[@class='by']//p)").extract()
		i['judul'] = response.xpath("string(//div[@class='wrap_detail_set']/h1)").extract_first()
		i['berita'] = response.xpath("normalize-space(//div[@class='artikel'])").extract()
		i['tag'] = response.xpath("//div[@class='wrap_blok_tag']//a/text()").extract()
		i['url'] = response.request.url
		i['website'] = 'republika'
		i['date'] = tanggal
		return i
