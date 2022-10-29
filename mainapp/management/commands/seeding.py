from django.core.management import BaseCommand
from mainapp.models import News


class Command(BaseCommand):

    def handle(self, *args, **options):
        for i in range(10):
            News.objects.create(
                title=f'news#{i}',
                preamble=f'preamble#{i}',
                body=f'this is for news#{i}'
            )
