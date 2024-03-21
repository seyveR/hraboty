import requests
import pymorphy2
from bs4 import BeautifulSoup
from ...models import Vacancy
from django.db import IntegrityError



class RabotaParser:
    def __init__(self):
        self.base_url = "https://www.rabota.ru/vacancy/?sort=relevance&all_regions=1"
        self.morph = pymorphy2.MorphAnalyzer()
        self.count = 0
        
    def parse_city_name(self, city_name):
        parsed = self.morph.parse(city_name)[0]
        if 'NOUN' in parsed.tag:
            return parsed.normal_form
        else:
            return city_name

    def get_page_count(self):
        page_content = requests.get(url=self.base_url).text
        pages = BeautifulSoup(page_content, features="lxml").findAll('a', {'class': 'pagination-list__item'})
        for page in pages:
            pg = page.text.strip()
        return int(pg)

    def parse_and_save_vacancies(self):
        for page_number in range(1, self.get_page_count() + 1):
            url = f"{self.base_url}&page={page_number}"
            page_content = requests.get(url=url).text
            soup = BeautifulSoup(page_content, features="lxml")
            text_blocks = soup.find('div', {'class': 'infinity-scroll r-serp__infinity-list'}).findAll('div', {'class': 'vacancy-preview-card__top'})
            
            for block in text_blocks:
                vacancy_url = "https://www.rabota.ru" + block.find('div', {'class': 'vacancy-preview-card__salary'}).find('a')['href']
                description = block.find('div', {'class': 'vacancy-preview-card__short-description'}).text
                self.save_vacancy_info(vacancy_url, description)
    
    def process_salary(self, value):
        # Разделяем значение по разделителю "—"
        values = value.split("—")

        # Проверяем количество значений
        if len(values) == 2:
            # Если есть два значения, убираем лишние пробелы
            salary_min = values[0].strip()
            salary_max = values[1].strip()
        else:
            # Если есть только одно значение, убираем лишние пробелы,
            # а второе значение устанавливаем как "Не указано"
            salary_min = values[0].strip()
            salary_max = "Не указано"

        try:int(salary_min.replace('От ', ''))
        except:salary_min = None
        
        try:int(salary_max)
        except:salary_max = None
        
        return salary_min, salary_max

    def save_vacancy_info(self, vacancy_url, description):
        page_content = requests.get(url=vacancy_url).text
        soup = BeautifulSoup(page_content, features="lxml")
        try: 
            employer =soup.find('div', {'class': 'vacancy-company-stats__name'}).find('a').text.strip().replace('ИНДИВИДУАЛЬНЫЙ ПРЕДПРИНИМАТЕЛЬ','ИП').replace('Индивидуальный предприниматель','ИП')
        except Exception: 
            employer =soup.find('div', {'class': 'vacancy-company-stats__name'}).find('span').text.strip().replace('ИНДИВИДУАЛЬНЫЙ ПРЕДПРИНИМАТЕЛЬ','ИП').replace('Индивидуальный предприниматель','ИП')
        try: 
            title =soup.find('div', {'class': 'branding-vacancy-card-header__title'}).find('h1').text.strip()
        except Exception: 
            title =soup.find('div', {'class': 'vacancy-card__title-header'}).find('h1').text.strip()
        try: 
            salary =soup.find('div', {'class': 'branding-vacancy-card-header__salary'}).find('h3').text.strip().replace(" руб.",'').replace('\xa0','').replace('—',' —')
        except Exception: 
            salary =soup.find('h3', {'class': 'vacancy-card__salary'}).text.strip().replace(" руб.",'').replace('\xa0','').replace('—',' —')
            
        salary_min, salary_max = self.process_salary(salary)
        
        try: 
            date =soup.find('span', {'class': 'vacancy-system-info__updated-date'}).meta.get('content').split('T')[0]
        except Exception: 
            print(vacancy_url)        
        
        area =self.parse_city_name(soup.find('title').text.strip().replace(f'Вакансия {title} в ','').split()[0]).capitalize()
        
        try: 
            schedule =soup.find('span', {'class': 'vacancy-requirements_uppercase'}).text.split(',')[0].strip().capitalize()
        except Exception: 
            schedule = "Не указано"
        
        
        # Извлекаем часть URL до параметра запроса, чтобы исключить его из проверки на уникальность
        vacancy_url_base = vacancy_url.split('?')[0]

        # Проверяем наличие записи с таким же базовым URL в базе данных
        if Vacancy.objects.filter(url__startswith=vacancy_url_base).exists():
            print(f"Rabota: {vacancy_url_base} already exists. Skipping...")
            return

        try:
            try:
                vacancy = Vacancy.objects.create(
                    name=title,
                    employer=employer,
                    url=vacancy_url,
                    salary_min=salary_min,
                    salary_max=salary_max,
                    description=description,
                    area=area,
                    schedule=schedule,
                    date=date
                )
                self.count += 1
                print(f"Rabota[{self.count}]: {title} saved successfully.")
            except Exception:
                print(vacancy_url + ' ERROR')
                pass
        except IntegrityError:
            print(f"Rabota: Failed to save vacancy {title}: IntegrityError.")
