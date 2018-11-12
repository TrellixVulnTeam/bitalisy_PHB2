from django.shortcuts import render
from django.http import HttpResponse
# Import Database
from scraping.models import NewsItem, TagNews, Lowonganku,KotaLowonganku

#Import for Google Trend
from pytrends.request import TrendReq

#import for Twitter API
import tweepy

import pandas as pd
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count, Sum
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import numpy as np


def home(request):
	'''Menuju ke Halaman Utama
	toptaglist : Mengambil 10 tag yang paling banyak muncul
	jumlahLowongan : jumlah Lowongan yang tersedia di database
	jumlahPerusahaan : jumlah Perusahaan yang tersedia di database (Satu perusahaan bisa memiliki beberapa lowongan)
	jumlah Pelamar : jumlah Pelamar yang tersedia di databasee
	'''
	toptaglist = TagNews.objects.values('tag').annotate(tag_count=Count('tag')).order_by('-tag_count')[:10]
	jumlahLowongan = Lowonganku.objects.count()
	jumlahPerusahaan =  Lowonganku.objects.aggregate(jumlah = Count('perusahaan'))	
	jumlahPelamar = Lowonganku.objects.aggregate(jumlah = Sum('jumlahPelamar'))
	return render(request, 'home.html', { 'toptaglist' : toptaglist, 'jumlahLowongan' : jumlahLowongan, 'jumlahPerusahaan':jumlahPerusahaan, 'jumlahPelamar':jumlahPelamar})

# @require_http_methods(['GET'])
def chartBerita(request):
	'''Membentuk chart bar berita (Jumlah Berita per Website)
	jumlahBerita : Mengambil jumlah berita dengan Group By nama_website
	Return berupa array dengan format tiap rownya (namaWebsite, jumlahBerita)
	'''
	jumlahBerita = NewsItem.objects.values('website').annotate(web_count=Count('website')).order_by('-web_count')
	beritaNamaPlot = []
	beritaJumlahPlot = []
	for x in jumlahBerita:
		website = x['website']
		web_count = x['web_count']
		beritaNamaPlot.append(website)
		beritaJumlahPlot.append(web_count)
	return JsonResponse({'beritaNamaPlot' : beritaNamaPlot, 'beritaJumlahPlot' : beritaJumlahPlot})

def homePagination(request):
	'''Mengambil berita dari database + mengatur pagination'''
	page = request.POST.get('page', 1)
	website_name = request.POST.get('website_name', 'all')
	beritaPerPage = 10
	if website_name == "all":
		'''Mengambil berita dari seluruh website'''
		beritalist = NewsItem.objects.all()[(int(page)-1)*int(beritaPerPage) : int(page)*int(beritaPerPage)]
		total = NewsItem.objects.count()
	else :
		'''Sortir berita berdasarkan website tertentu'''
		beritalist = NewsItem.objects.filter(website = website_name)[(int(page)-1)*int(beritaPerPage) : int(page)*int(beritaPerPage)]
		total = NewsItem.objects.filter(website = website_name).count()
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

def twitterAPI(request):
	auth = tweepy.OAuthHandler('lJQGdnHBAzZdWvnd5UKXKtskh', 'BInaMZF8iwtaO6xuE4LjpS6A3s7WyN8ig4stKfHwL3K9FORnkN')
	auth.set_access_token('1165843525-BoS3Am809TpRz8SvHAxouQqEi6iWwUoT2mZOlXy', '9N6PDDf4NIrMkTjpcHJiDmiJ0a7timVAzGEGwCTCQ8Cvc')
	api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
	# geoID didapatkan dari 
	# places = api.geo_search(query="Indonesia", granularity="country")
	# place_id = places[0].id
	keyword = request.POST.get('keywordTwitter', 'kerja')
	lower = keyword.lower()
	upper = keyword.upper()
	capitalize = keyword.capitalize()
	# searchQuery = 'place:ce7988d3a8b6f49f kerja OR Kerja OR KERJA'
	searchQuery = 'place:ce7988d3a8b6f49f '+lower+' OR '+upper+' OR '+capitalize
	# maxTweets = 1000000
	maxTweets = 10
	tweetsPerQry = 100
	statusTweet = []
	dataTwitter = []
	trendTwitter = []
	tweetCount = 0
	z = tweepy.Cursor(api.search,q=searchQuery).items(maxTweets)
	# print(z[0])
	print("Test3.1")
	for tweet in z :
		if tweet.place is not None:
			row = {
				'tweet' : tweet.text,
				'user' : tweet.user.screen_name,
				'lokasi' : tweet.place.full_name,
				'tanggal' : tweet.created_at,
				# tweet.entities['urls'][0]['url']
			}
			dataTwitter.append(row)
			tweetCount += 1
			# statusTweet.append(tweet.text)
	#23424846 adalah WOEID Indonesia. Didapatkan dari http://woeid.rosselliot.co.nz/lookup/indonesia
	trends = api.trends_place(23424846)
	for trend in trends[0]['trends']:
		row = {
			'trend' : trend['name'],
			'jumlah' : trend['tweet_volume'],
			'url' : trend['url'],
		}
		trendTwitter.append(row)
	return JsonResponse({'tweetCount':tweetCount,'dataTwitter' : dataTwitter[0:10], 'trendTwitter' : trendTwitter})
	# return JsonResponse({'statusTweet' : "Success"})
