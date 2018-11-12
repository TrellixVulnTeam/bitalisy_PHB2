"""Bitalisy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls import url,static

from monitoring import views as monitoringViews
from scraping import views as scrapingViews
from pencarian import views as pencarianViews
from tabulasi import views as tabulasiViews


urlpatterns = [
	url(r'^$', monitoringViews.home, name='home'),
    url(r'^monitoring/twitterAPI', monitoringViews.twitterAPI, name='twitterAPI'),
    url(r'^homePagination/$', monitoringViews.homePagination, name='homePagination'),
    url(r'^chartBerita/$', monitoringViews.chartBerita, name='chartBerita'),
    url(r'^chartPieLowongan/$', monitoringViews.chartPieLowongan, name='chartPieLowongan'),
    url(r'^chartPerusahaanFavorit/$', monitoringViews.chartPerusahaanFavorit, name='chartPerusahaanFavorit'),
    url(r'^chartLineGoogle/$', monitoringViews.chartLineGoogle, name='chartLineGoogle'),
    url(r'^tabulasi/berita/$', tabulasiViews.tabulasiBerita, name='tabulasiBerita'),
    url(r'^tabulasi/berita/detail/$', tabulasiViews.detailBerita, name='detailBerita'),
    url(r'^tabulasi/lowongan/$', tabulasiViews.tabulasiLowongan, name='tabulasiLowongan'),
    url(r'^jumlahBerita/', tabulasiViews.jumlahBerita, name='jumlahBerita'),
	url(r'^api/crawl/$', scrapingViews.crawl, name='crawl'),
    url(r'^api/Jobcrawl/$', scrapingViews.Jobcrawl, name='Jobcrawl'),
	url(r'^scraping/berita/$', scrapingViews.scrapsBerita, name='scrapsBerita'),
    url(r'^scraping/lowongan/$', scrapingViews.scrapsLowongan, name='scrapsLowongan'),
    url(r'^pencarian/$', pencarianViews.pencarian, name='pencarian'),
    url(r'^loadBerita/$', pencarianViews.loadBerita, name='loadBerita'),
    path('admin/', admin.site.urls),
]
