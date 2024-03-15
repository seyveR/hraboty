from .rabota import RabotaParser
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Парсинг'
    
    def handle(self, *args, **options):
        parser = RabotaParser()
        page_count = parser.get_page_count()
        for page_number in range(1, page_count + 1):
            parser.parse_and_save_vacancies(page_number)
