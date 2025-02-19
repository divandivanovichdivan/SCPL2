import requests
import time
from terminaltables import AsciiTable
from dotenv import load_dotenv
import os


def predict_rub_salary(salary_from, salary_to):
    if salary_from and salary_to:
        expected_salary = (salary_from + salary_to) / 2
    elif salary_to:
        expected_salary = salary_to * 0.8
    elif salary_from:
        expected_salary = salary_from * 1.2
    else:
        expected_salary = None
    return expected_salary


def predict_rub_salary_hh(vacancy):
    salary = vacancy["salary"]
    if salary is not None:
        salary_from, salary_to = salary["from"], salary["to"]
        expected_salary = predict_rub_salary(salary_from, salary_to)
    else:
        expected_salary = None
    return expected_salary


def predict_rub_salary_sj(vacancy):
    payment_from, payment_to = vacancy["payment_from"], vacancy["payment_to"]
    expected_salary = predict_rub_salary(payment_from, payment_to)
    return expected_salary


def bild_a_table(table_data, title):
    table = AsciiTable(table_data, title)
    table.inner_heading_row_border = True
    print(table.table)


def print_a_sj_table(languages, sj_table_data, headers):
    payload = {
            "town": "Москва",
            "page": 0,
            "per_page": 10,
            "keyword": None
    }
    url = "https://api.superjob.ru/2.0/vacancies/"
    for language in languages:
        payload["keyword"] = language
        payload["page"] = 0
        vacancies_col = 0
        vacancies_processed = 0
        salaries_sum = 0
        while payload["page"] < 55:
            response = requests.get(url, params=payload, headers=headers)
            response.raise_for_status()
            objects = response.json()["objects"]
            for vacancy in objects:
                expected_salary = predict_rub_salary_sj(vacancy)
                vacancies_col += 1
                if expected_salary is not None:
                    vacancies_processed += 1
                    salaries_sum += expected_salary
            payload["page"] += 1
        if vacancies_processed != 0:
            average_salary = salaries_sum // vacancies_processed
        else:
            average_salary = None
        sj_table_data.append([
            language,
            vacancies_col,
            vacancies_processed,
            average_salary
            ])
    bild_a_table(sj_table_data, "Superjob Moscow")


def print_a_hh_table(languages, hh_table_data):
    payload = {
        "professional_role": 96,
        "area": 1,
        "period": 28,
        "text": None,
        "page": 0,
        "per_page": 100
        }
    for language in languages:
        time.sleep(1)
        payload["text"] = language
        vacancies_col = 0
        salaries_sum = 0
        vacancies_processed = 0
        vacancies = {
                "items": True
            }
        while vacancies["items"] != [] and payload["page"] != 20:
            response = requests.get(
                "https://api.hh.ru/vacancies",
                params=payload)
            response.raise_for_status()
            vacancies = response.json()
            for vacancy in vacancies["items"]:
                expected_salary = predict_rub_salary_hh(vacancy)
                vacancies_col += 1
                if expected_salary is not None:
                    vacancies_processed += 1
                    salaries_sum += expected_salary
            payload["page"] += 1
        payload["page"] = 0
        vacancies_found = vacancies.get("found", 0)
        if vacancies_processed != 0:
            average_salary = salaries_sum // vacancies_processed
        else:
            average_salary = 0
        hh_table_data.append([
            language,
            vacancies_col,
            vacancies_processed,
            average_salary])
    bild_a_table(hh_table_data, "HeadHunter Moscow")


def main():
    load_dotenv()
    sj_headers = {
            "X-Api-App-Id": os.environ["CLIENT_SECRET"],
        }
    global_table_data = [
        [
            "Язык программирования",
            "Вакансий найдено",
            "Вакансий обработано",
            "Средняя зарплата"
            ]
        ]
    languages = [
        "JavaScript",
        "Java",
        "Python",
        "Ruby",
        "PHP",
        "C++",
        "C#",
        "TypeScript"
        ]
    print_a_sj_table(languages, global_table_data, sj_headers)
    print()
    global_table_data = [
        [
            "Язык программирования",
            "Вакансий найдено",
            "Вакансий обработано",
            "Средняя зарплата"
            ]
        ]
    print_a_hh_table(languages, global_table_data)


if __name__ == "__main__":
    main()
    