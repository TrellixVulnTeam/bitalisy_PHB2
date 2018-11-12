from import_export import resources
from scraping.models import NewsItem

class NewsResource(resources.ModelResource):
    class Meta:
        model = NewsItem