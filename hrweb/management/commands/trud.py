import requests
import json 
import re
import math
from ...models import Vacancy
from django.db import IntegrityError

class TrudvsemParser:
    def __init__(self):
        self.base_url = "https://opendata.trudvsem.ru/api/v1/vacancies"
        self.count = 0

    def parse_and_save_vacancies(self):
        for page_number in range(100):
            url = f"{self.base_url}?offset={page_number}"
            req = requests.get(url)
            data = req.json()
            req.close()

            if data['status'] == '200':
                vacancies = data['results']['vacancies']
                for vac in vacancies:
                    name = vac['vacancy']['job-name']
                    employer = vac['vacancy']['company']['name']
                    url = vac['vacancy']['vac_url']
                    
                    salary_max = vac['vacancy'].get('salary_max', None) or None
                    salary_min = vac['vacancy'].get('salary_min', None) or None
                    
                    try:
                        description = re.sub(r'<[^>]*>', '', vac['vacancy']['duty']).replace("&bull;",'').replace("\n",' ').replace("\r",'').replace("&nbsp;",'').replace('&middot','')
                    except Exception as ex:
                        description = 'Не указано'
                    try:
                        area = (vac['vacancy']['region']['name']).replace('Город ', '')
                    except:
                        area = 'Не указано'
                    date = vac['vacancy']['creation-date']
                    schedule = vac['vacancy']['schedule']

                    self.save_vacancy_info(name, employer, url, salary_min, salary_max, description, area, date, schedule)
            else:
                break

    def save_vacancy_info(self, name, employer, url, salary_min, salary_max, description, area, date, schedule):
        # Проверяем наличие записи с таким же URL в базе данных
        if Vacancy.objects.filter(url=url).exists():
            print(f"Trudvsem: {url} already exists. Skipping...")
            return

        try:
            vacancy = Vacancy.objects.create(
                name=name,
                employer=employer,
                url=url,
                salary_min=salary_min,
                salary_max=salary_max,
                description=description,
                area=area,
                date=date,
                schedule=schedule
            )
            self.count += 1
            print(f"Trudvsem[{self.count}]: {name} saved successfully.")
        except IntegrityError:
            # Если возникает ошибка IntegrityError, значит запись была создана в другом потоке/процессе
            print(f"Trudvsem: Failed to save vacancy {name}: IntegrityError.")
