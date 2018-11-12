# -*- coding: utf-8 -*-

# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scraping.models import NewsItem, linkURL, TagNews
import json

class ScrapyAppPipeline(object):
	def __init__(self, unique_id, *args, **kwargs):
		print("Mulai Scraping")

	@classmethod
	def from_crawler(cls, crawler):
		return cls(
			unique_id=crawler.settings.get('unique_id'), # this will be passed from django view
		)

	# def close_spider(self, spider):
	#     i, created_i = linkURL.objects.get_or_create(link=url)
	#         # if created_i :
	#             # i.save()

	def process_item(self, item, spider):
		# Mengecek apakah berita ada di database
		d, created = NewsItem.objects.get_or_create(date = item['date'], url=item['url'])
		# Jika created -> berita tidak ada di database, maka akan disimpan
		if created:
			d.breadcrumbs=item['breadcrumbs']
			d.penulis = item['penulis']
			d.judul = item['judul']
			d.berita = item['berita']
			d.tag = item['tag']
			d.website = item['website']
			d.save()
			# Satu Berita memiliki banyak tag, maka tag dipisah ke tabel lainnya
			for t in item['tag']:
				url = NewsItem.objects.last()
				y = TagNews.objects.create(tag = t, url=url)
				y.save()
		return item
