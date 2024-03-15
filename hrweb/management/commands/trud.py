import requests
import json 
import re
import math
from ...models import Vacancy
from django.db import IntegrityError

class TrudvsemParser:
    def __init__(self):
        self.base_url = "https://opendata.trudvsem.ru/api/v1/vacancies"

    def get_vacancy_count(self):
        req = requests.get(self.base_url)
        data = req.json()
        req.close()
        total_vacancies = data['meta']['total']
        return total_vacancies

    def parse_and_save_vacancies(self):
        total_vacancies = self.get_vacancy_count()
        max_page = math.ceil(total_vacancies / 100)

        for page_number in range(1, max_page + 1):
            url = f"{self.base_url}?offset={(page_number - 1) * 100}"
            req = requests.get(url)
            data = req.json()
            req.close()

            if data['status'] == '200':
                vacancies = data['results']['vacancies']
                for vac in vacancies:
                    name = vac['vacancy']['job-name']
                    employer = vac['vacancy']['company']['name']
                    url = vac['vacancy']['vac_url']
                    if vac['vacancy']['salary_max'] == 0:
                        salary = vac['vacancy']['salary_min']
                    else:
                        salary = vac['vacancy']['salary_max']
                    try:
                        description = re.sub(r'<[^>]*>', '', vac['vacancy']['duty']).replace("\n",' ').replace("\r",'').replace("&nbsp;",'').replace('&middot','')
                    except Exception as ex:
                        description = 'Не указано'
                    try:
                        area = vac['vacancy']['region']['name']
                    except:
                        area = 'Не указано'
                    date = vac['vacancy']['creation-date']

                    self.save_vacancy_info(name, employer, url, salary, description, area, date)
            else:
                break

    def save_vacancy_info(self, name, employer, url, salary, description, area, date):
        # Проверяем наличие записи с таким же URL в базе данных
        if Vacancy.objects.filter(url=url).exists():
            print(f"Vacancy with URL {url} already exists. Skipping...")
            return

        try:
            vacancy = Vacancy.objects.create(
                name=name,
                employer=employer,
                url=url,
                salary=salary,
                description=description,
                area=area,
                date=date
            )
            print(f"Vacancy {name} saved successfully.")
        except IntegrityError:
            # Если возникает ошибка IntegrityError, значит запись была создана в другом потоке/процессе
            print(f"Failed to save vacancy {name}: IntegrityError.")
