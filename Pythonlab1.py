from bs4 import BeautifulSoup
import requests
import pandas as pd

def parse_vacancies():
    url = 'https://hh.ru/search/vacancy?text=Python&area=1'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    page = requests.get(url, headers=headers)

    soup = BeautifulSoup(page.text, "html.parser")
    vacancies = soup.find_all('div', class_='magritte-redesign')

    vacancies_list = []
    for vacancy in vacancies:
        title = vacancy.find('h2', {'data-qa': 'bloko-header-2'}).text.strip()
        company = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-employer'}).text.strip()
        location = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-address'}).text.strip()
        salary = vacancy.find('span', class_='magritte-text___pbpft_3-0-27 magritte-text_style-primary___AQ7MW_3-0-27 magritte-text_typography-label-1-regular___pi3R-_3-0-27')
        salary = salary.text.strip() if salary else 'Не указано'

        vacancies_list.append({
            'Название вакансии': title,
            'Компания': company,
            'Местоположение': location,
            'Зарплата': salary
        })

    df = pd.DataFrame(vacancies_list)
    df.to_excel('vacancies.xlsx', index=False)

parse_vacancies()
