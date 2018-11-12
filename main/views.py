from uuid import uuid4
from urllib.parse import urlparse
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_POST, require_http_methods
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from scrapyd_api import ScrapydAPI
# from main.utils import URLUtil
from scraping.models import NewsItem, linkURL

# connect scrapyd service
scrapyd = ScrapydAPI('http://localhost:6800')

def home(request):

	return render(request, 'home.html')	

def is_valid_url(url):
	validate = URLValidator()
	try:
		validate(url) # check if url format is valid
	except ValidationError:
		return False

	return True


@csrf_exempt
@require_http_methods(['POST', 'GET']) # only get and post
def crawl(request):
	# Post requests are for new crawling tasks
	if request.method == 'POST':

		url = request.POST.get('url', None) # take url comes from client. (From an input may be?)
		website = request.POST.get('website', None)
		#Cek apakah benar benar url
		if not url:
			return JsonResponse({'error': 'Missing  args'})
		
		# Cek apakah url valid
		if not is_valid_url(url):
			return JsonResponse({'error': 'URL is invalid'})
		
		# Cek apakah url sudah
		if linkURL.objects.filter(link=url).exists():
			return JsonResponse({'error': 'URL sudah tersimpan dalam database'})
		# else:
			# print("Hello World")
			# d, created = linkURL.objects.get_or_create(link=url)
			# if created :
			# 	d.save()			

		# return JsonResponse({'DIA MASIH DISINI': '0.1'})
		domain = urlparse(url).netloc # parse the url and extract the domain
		unique_id = str(uuid4()) # create a unique ID. 
		# return JsonResponse({'DIA MASIH DISINI': '0.2'})
		# This is the custom settings for scrapy spider. 
		# We can send anything we want to use it inside spiders and pipelines. 
		# I mean, anything
		settings = {
			'unique_id': unique_id, # unique ID for each record for DB
			'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
		}
		# return JsonResponse({'DIA MASIH DISINI': '1'})
		# Here we schedule a new crawling task from scrapyd. 
		# Notice that settings is a special argument name. 
		# But we can pass other arguments, though.
		# This returns a ID which belongs and will be belong to this task
		# We are goint to use that to check task's status.
		task = scrapyd.schedule("default", website, settings=settings, url=url, domain=domain)
		# return JsonResponse({'DIA MASIH DISINI': '2'})

		return JsonResponse({'task_id': task, 'unique_id': unique_id, 'status': 'started' })
		# return JsonResponse({'DIA MASIH DISINI': '3'})
		# return render

	# Get requests are for getting result of a specific crawling task
	elif request.method == 'GET':
		# We were passed these from past request above. Remember ?
		# They were trying to survive in client side.
		# Now they are here again, thankfully. <3
		# We passed them back to here to check the status of crawling
		# And if crawling is completed, we respond back with a crawled data.
		task_id = request.GET.get('task_id', None)
		unique_id = request.GET.get('unique_id', None)
		url = request.GET.get('url', None)

		if not task_id or not unique_id:
			return JsonResponse({'error': 'Missing args'})

		# Here we check status of crawling that just started a few seconds ago.
		# If it is finished, we can query from database and get results
		# If it is not finished we can return active status
		# Possible results are -> pending, running, finished
		status = scrapyd.job_status('default', task_id)
		if status == 'finished':
			# d, created = linkURL.objects.get_or_create(link=url)
			# if created :
				# d.save()
			return JsonResponse({'data': url, 'statusCrawling':'finished'})
		else:
			return JsonResponse({'status': status})
