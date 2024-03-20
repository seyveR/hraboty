from .rabota import RabotaParser
from .trud import TrudvsemParser
from .hh import HHParser
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Запуск парсеров'
    
    def handle(self, *args, **options):
        parsers = [HHParser(), RabotaParser(), TrudvsemParser()]

        # Запускаем парсеры
        for parser in parsers:
            parser.parse_and_save_vacancies()
