import json
from django.db import models
from django.utils import timezone

class linkURL(models.Model):
	link = models.TextField(unique = True)
	date = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.link
class NewsItem(models.Model):
	breadcrumbs = models.CharField(max_length=150, null=True)
	penulis = models.CharField(max_length=100, null=True)
	judul = models.CharField(max_length=200, null=True)
	berita = models.TextField()
	tag = models.CharField(max_length=100, null=True)
	url = models.CharField(max_length=200, unique = True)
	website = models.CharField(max_length=50, null=True)
	date = models.DateTimeField()
	@property
	def to_dict(self):
		data = {
			'data': json.loads(self.url),
			'tanggal': self.tanggal
		}
		return data

	def __str__(self):
		return self.url
# view rawmodels.py hosted with ❤ by GitHubnnlknsldnlsndlnslkdnlksndklnsldnlndsklknkndslknkldnlksndlk