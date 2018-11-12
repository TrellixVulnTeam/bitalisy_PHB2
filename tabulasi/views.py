from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count, Sum
from django.http import JsonResponse
from datetime import datetime
from scraping.models import NewsItem, Lowonganku

# Create your views here.
def tabulasiBerita(request):
	'''Mengarahan ke halaman Tabulasi Berita'''
	return render(request, 'tabulasi_berita.html') 

def tabulasiLowongan(request):
	'''Mengarahkan ke Tabulasi Lowongan'''
	lowonganList = Lowonganku.objects.all()
	return render(request, 'tabulasi_lowongan.html', {'lowonganList' : lowonganList})

def jumlahBerita(request):
	'''Mengambil jumlah berita per Bulannya'''
	month = request.POST.get('month', None)
	year = request.POST.get('year', None)

	berita = NewsItem.objects.filter(date__year=year).filter(date__month=month)
	total = berita.extra({'created':"date(date)"}).values('created','website').annotate(jumlah=Count('url')).order_by('created')

	result = []
	for x in total:
		row = {
			'jumlah' : x['jumlah'],
			'date' : x['created'],
			'website' : x['website'],
		}
		result.append(row)

	# Untuk Berita dari detik
	jumlahdetik = []
	tanggaldetik = []
	for x in total.filter(website='detik'):
		jumlahdetik.append(x['jumlah'])
		tanggaldetik.append(x['created'])

	# Untuk Berita dari Kompas
	jumlahkompas = []
	tanggalkompas = []
	for x in total.filter(website='kompas'):
		jumlahkompas.append(x['jumlah'])
		tanggalkompas.append(x['created'])

	# Untuk Berita dari Republika
	jumlahrepublika = []
	tanggalrepublika = []
	for x in total.filter(website='republika'):
		jumlahrepublika.append(x['jumlah'])
		tanggalrepublika.append(x['created'])

	# Untuk Berita dari Sindo
	jumlahsindo = []
	tanggalsindo = []
	for x in total.filter(website='sindo'):
		jumlahsindo.append(x['jumlah'])
		tanggalsindo.append(x['created'])

	# Untuk Berita dari Tribun
	jumlahtribun = []
	tanggaltribun = []
	for x in total.filter(website='tribun'):
		jumlahtribun.append(x['jumlah'])
		tanggaltribun.append(x['created'])

	# Untuk Berita dari Okezone
	jumlahokezone = []
	tanggalokezone = []
	for x in total.filter(website='okezone'):
		jumlahokezone.append(x['jumlah'])
		tanggalokezone.append(x['created'])

	return JsonResponse({'month':month,'year':year, 'result':result, 'detik':jumlahdetik, 'tanggalDetik':tanggaldetik, 'kompas':jumlahkompas, 'tanggalKompas':tanggalkompas, 'republika':jumlahrepublika,'tanggalRepublika':tanggalrepublika,'sindo':jumlahsindo,'tanggalSindo':tanggalsindo,'tribun':jumlahtribun,'tanggalTribun':tanggaltribun,'okezone':jumlahokezone,'tanggalOkezone':tanggalokezone})

def detailBerita(request):
	'''Mengambil detail dari berita yakni isi berita, judul penulis,tag, dll'''
	namaWeb = request.POST.get('website', None)
	tanggal = request.POST.get('tanggal', None)
	hasil = datetime.strptime(tanggal, "%Y-%m-%d")
	beritalist = NewsItem.objects.filter(website = namaWeb).filter(date__date= hasil)
	tanggalBerita = hasil.strftime("%d/%m/%Y")
	return render(request, 'tabulasi_berita_detail.html', {'beritalist':beritalist, 'website':namaWeb, 'tanggal':tanggalBerita})