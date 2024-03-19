import requests
import json 
import re
import math
from ...models import Vacancy
from django.db import IntegrityError



class HHParser:
    def __init__(self):
        self.base_url = "https://api.hh.ru/vacancies"
        
    def deEmojify(self, text):
        emoji_pattern = re.compile("["
                    u"\U0001F600-\U0001F64F"
                    u"\U0001F300-\U0001F5FF"
                    u"\U0001F680-\U0001F6FF"
                    u"\U0001F1E0-\U0001F1FF"
                    u"\U00002702-\U000027B0"
                    u"\U000024C2-\U0001F251"
                    u"\U0001f926-\U0001f937"
                    u'\U00010000-\U0010ffff'
                    u"\u200d"
                    u"\u2640-\u2642"
                    u"\u2600-\u2B55"
                    u"\u23cf"
                    u"\u23e9"
                    u"\u231a"
                    u"\u3030"
                    u"\ufe0f"
                    u"\u2012""]+", flags=re.UNICODE)
        return emoji_pattern.sub(r'',text)

    def parse_and_save_vacancies(self):
        req = requests.get(self.base_url)
        data = req.content.decode()
        req.close()
        data = json.loads(data)    
        try:
            req = requests.get(self.base_url)
            data = req.content.decode()
            req.close()
            data = json.loads(data)
            vacancies = data['items']
            for vac in vacancies:
                name = vac['name']
                employer = vac['employer']['name']
                url = vac['alternate_url']
                try:
                    salary = vac['salary']['from']
                except Exception:
                    salary = 'Не указано'
                area = vac['area']['name']
                description = self.deEmojify(re.sub(r'\<[^>]*\>', '', str(f"Требования: {vac['snippet']['requirement']} Обязанности: {vac['snippet']['responsibility']}")))
                date = (vac['published_at']).split('T')[0]
                schedule = vac['schedule']['name']
                self.save_vacancy_info(name, employer, url, salary, description, area, date, schedule)
        except Exception:
            pass

    def save_vacancy_info(self, name, employer, url, salary, description, area, date, schedule):
        # Проверяем наличие записи с таким же URL в базе данных
        if Vacancy.objects.filter(url=url).exists():
            print(f"{url} already exists. Skipping...")
            return

        try:
            vacancy = Vacancy.objects.create(
                name=name,
                employer=employer,
                url=url,
                salary=salary,
                description=description,
                area=area,
                date=date,
                schedule=schedule
            )
            print(f"{name} saved successfully.")
        except IntegrityError:
            # Если возникает ошибка IntegrityError, значит запись была создана в другом потоке/процессе
            print(f"Failed to save vacancy {name}: IntegrityError.")
