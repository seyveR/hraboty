import requests
import json 
import re
import math
from ...models import Vacancy
from django.db import IntegrityError



class HHParser:
    def __init__(self):
        self.base_url = "https://api.hh.ru/vacancies?per_page=100&area=113"
<<<<<<< HEAD
        self.count = 0
=======
>>>>>>> main
        
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
        max_pages = int(data['pages'])
        try:
            for i in range(max_pages):
                req = requests.get(self.base_url+f'&page={i}')
                data = req.content.decode()
                req.close()
                data = json.loads(data)
                vacancies = data['items']
                for vac in vacancies:
                    name = vac['name']
                    employer = vac['employer']['name']
                    url = vac['alternate_url']
                    
                    try: salary_min = vac['salary']['from']
                    except Exception: salary_min = None
<<<<<<< HEAD
                    salary_min = salary_min if salary_min is not None else None

                    try: salary_max = vac['salary']['to']
                    except Exception: salary_max = None
                    salary_max = salary_max if salary_max is not None else None
=======
                    salary_min = float(salary_min) if salary_min is not None else None

                    try: salary_max = vac['salary']['to']
                    except Exception: salary_max = None
                    salary_max = float(salary_max) if salary_max is not None else None

                    # salary_min = vac['salary']['from']
                    # if salary_min is not None:
                    #     salary_min = float(salary_min)
                    
                    # salary_max = vac['salary']['to']
                    # if salary_max is not None:
                    #     salary_max = float(salary_max)
>>>>>>> main

                    area = vac['area']['name']
                    description = self.deEmojify(re.sub(r'\<[^>]*\>', '', str(f"Требования: {vac['snippet']['requirement']} Обязанности: {vac['snippet']['responsibility']}")))
                    date = (vac['published_at']).split('T')[0]
                    schedule = vac['schedule']['name']
<<<<<<< HEAD
                    
                    role = vac['professional_roles'][0]['name']
                    role = 'Не указано' if role == 'Другое' else role
                    self.save_vacancy_info(name, employer, url, salary_min, salary_max, description, area, date, schedule, role)
        except Exception:
            pass

    def save_vacancy_info(self, name, employer, url, salary_min, salary_max, description, area, date, schedule,role):
=======
                    self.save_vacancy_info(name, employer, url, salary_min, salary_max, description, area, date, schedule)
                    print("Name:", name)
                    print("Employer:", employer)
                    print("URL:", url)
                    print("Salary Min:", salary_min)
                    print("Salary Max:", salary_max)
                    print("Salary Type:", type(salary_min))
                    print("Area:", area)
                    print("Description:", description)
                    print("Date:", date)
                    print("Schedule:", schedule)
                    print("\n")
        except Exception:
            pass

    def save_vacancy_info(self, name, employer, url, salary_min, salary_max, description, area, date, schedule):
>>>>>>> main
        # Проверяем наличие записи с таким же URL в базе данных
        if Vacancy.objects.filter(url=url).exists():
            print(f"HH: {url} already exists. Skipping...")
            return

        try:
            #print(salary_min, salary_max)
            vacancy = Vacancy.objects.create(
                name=name,
                employer=employer,
                url=url,
                salary_min=salary_min,
                salary_max=salary_max,
                description=description,
                area=area,
                date=date,
<<<<<<< HEAD
                schedule=schedule,
                role=role
                )
            self.count += 1
            print(f"HH[{self.count}]: {name} saved successfully.")
        except IntegrityError:
            # Если возникает ошибка IntegrityError, значит запись была создана в другом потоке/процессе
            print(f"HH: Failed to save vacancy {name}: IntegrityError.")
=======
                schedule=schedule
            )
            print(f"HH: {name} saved successfully.")
        except IntegrityError:
            # Если возникает ошибка IntegrityError, значит запись была создана в другом потоке/процессе
            print(f"HH: Failed to save vacancy {name}: IntegrityError.")
>>>>>>> main
