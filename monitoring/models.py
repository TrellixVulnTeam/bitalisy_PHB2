from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Berita(models.Model):
	url = models.CharField(max_length=200, unique = True)
	breadcrumb = models.CharField(max_length=100) 
	tanggal = models.DateTimeField(null=True)
	penulis = models.CharField(max_length=50)
	judul = models.CharField(max_length=200)
	isi = models.TextField(max_length=4000)
	
	def __str__(self):
		return self.url
class Tag(models.Model):
	tag = models.CharField(max_length=50)
	url = models.ForeignKey(Berita, on_delete=models.CASCADE, related_name = 'tags')

	def __str__(self):
		return self.tag

class Person(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    birth_date = models.DateField()
    location = models.CharField(max_length=100, blank=True)
