from django.shortcuts import render
from django.http import HttpResponse
# from django.views.decorators.csrf import csrf_exempt
from scraping.models import NewsItem, TagNews, Lowonganku,KotaLowonganku
from django.db.models import Count, Sum
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from .resources import NewsResource
# import csv
# from django.contrib.auth.models import User


# Create your views here.

def pencarian(request):
	'''Membuka halaman pencarian'''
	if request.method == 'POST':
		keyword = request.POST.get('keyword',None)
		return render(request, 'pencarian.html', {'keyword' : keyword})
	else :
		return render(request, 'pencarian.html')

def loadBerita(request):
	'''Mengambil berita sesuai dengan pencarian
	page : Melihat halaman berapa (Per halaman ditentukan oleh beritaPerPage)
	beritaPerPage : menentukan berapa banyak berita per halaman
	website_name : Menentukan website mana yang dilakukan pencarian
	startDate : Digunakan untuk sortir berita dari tanggal tersebut
	endDate : Digunakan untuk sortir berita sebelum tanggal tersebut
	'''
	page = request.POST.get('page', 1)
	beritaPerPage = 10
	website_name = request.POST.get('website_name', 'all')
	keyword = request.POST.get('keyword', None)
	startDate = request.POST.get('startDate', None)
	endDate = request.POST.get('endDate', None)

	if startDate : 
		if endDate :
		# Ada Tanggal Awal dan Akhir
			if website_name == "all":
				# Ada Tanggal Awal dan Akhir + Semua Web
				beritalist = NewsItem.objects.filter(judul__iregex=r'\s{}\s'.format(keyword)).filter(date__date__gte = startDate).filter(date__date__lte = endDate)[(int(page)-1)*int(beritaPerPage) : int(page)*int(beritaPerPage)]
				total = NewsItem.objects.filter(judul__iregex=r'\s{}\s'.format(keyword)).filter(date__date__gte = startDate).filter(date__date__lte = endDate).count()
			else :
				# Ada Tanggal Awal dan Akhir + Web Tertentu
				beritalist = NewsItem.objects.filter(judul__iregex=r'\s{}\s'.format(keyword)).filter(website = website_name).filter(date__date__gte = startDate).filter(date__date__lte = endDate)[(int(page)-1)*int(beritaPerPage) : int(page)*int(beritaPerPage)]
				total = NewsItem.objects.filter(judul__iregex=r'\s{}\s'.format(keyword)).filter(website = website_name).filter(date__date__gte = startDate).filter(date__date__lte = endDate).count()
		else :
		# Hanya ada Tanggal Awal
			if website_name == "all":
				# Ada Tanggal Awal dan Akhir + Semua Web
				beritalist = NewsItem.objects.filter(judul__iregex=r'\s{}\s'.format(keyword)).filter(date__date__gte = startDate)[(int(page)-1)*int(beritaPerPage) : int(page)*int(beritaPerPage)]
				total = NewsItem.objects.filter(judul__iregex=r'\s{}\s'.format(keyword)).filter(date__date__gte = startDate).count()
			else :
				# Ada Tanggal Awal dan Akhir + Web Tertentu
				beritalist = NewsItem.objects.filter(judul__iregex=r'\s{}\s'.format(keyword)).filter(website = website_name).filter(date__date__gte = startDate)[(int(page)-1)*int(beritaPerPage) : int(page)*int(beritaPerPage)]
				total = NewsItem.objects.filter(judul__iregex=r'\s{}\s'.format(keyword)).filter(website = website_name).filter(date__date__gte = startDate).count()
	elif website_name == "all":
		#Tidak ada tanggal Awal dan akhir + Semua Web
		beritalist = NewsItem.objects.filter(judul__iregex=r'\s{}\s'.format(keyword))[(int(page)-1)*int(beritaPerPage) : int(page)*int(beritaPerPage)]
		total = NewsItem.objects.filter(judul__iregex=r'\s{}\s'.format(keyword)).count()
	else :
		#Tidak ada tanggal Awal dan akhir + Web tertentu
		beritalist = NewsItem.objects.filter(judul__iregex=r'\s{}\s'.format(keyword)).filter(website = website_name)[(int(page)-1)*int(beritaPerPage) : int(page)*int(beritaPerPage)]
		total = NewsItem.objects.filter(judul__iregex=r'\s{}\s'.format(keyword)).filter(website = website_name).count()
	# beritalist = NewsItem.objects.all()[0:10]
	
	result = []
	tagresult = []
	for x in beritalist:
		row = {
			'judul' : x.judul,
			'url' : x.url,
			'date' : x.date,
			'website' : x.website,
			'berita' :x.berita,
 		}
		result.append(row)
		tags = []
		for y in x.tags.all():
			taglist = {
				'tags' : y.tag
			}
			tags.append(taglist)
		tagresult.append(tags)
	return JsonResponse({'tags':tagresult,'beritaList' : result, 'total' : total, 'beritaPerPage' : beritaPerPage, 'website_name' : website_name})


# def export(request):
#     person_resource = NewsResource()
#     dataset = person_resource.export()
#     response = HttpResponse(dataset.csv, content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="persons.csv"'
#     return response
