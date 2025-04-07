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
    if salary:
        salary_from, salary_to = salary["from"], salary["to"]
        expected_salary = predict_rub_salary(salary_from, salary_to)
    else:
        expected_salary = None
    return expected_salary


def predict_rub_salary_sj(vacancy):
    payment_from, payment_to = vacancy["payment_from"], vacancy["payment_to"]
    expected_salary = predict_rub_salary(payment_from, payment_to)
    return expected_salary


def get_sj_language_stat(language, payload, headers):
    url = "https://api.superjob.ru/2.0/vacancies/"
    vacancies_processed = 0
    salaries_sum = 0
    vacancies = {
            "more": True
        }
    while vacancies["more"]:
        response = requests.get(url, params=payload, headers=headers)
        response.raise_for_status()
        vacancies = response.json()
        for vacancy in vacancies["objects"]:
            expected_salary = predict_rub_salary_sj(vacancy)
            if expected_salary:
                vacancies_processed += 1
                salaries_sum += expected_salary
        payload["page"] += 1
    vacancies_number = vacancies["total"]
    return vacancies_number, vacancies_processed, salaries_sum


def get_hh_language_stat(language, payload):
    salaries_sum = 0
    vacancies_processed = 0
    vacancies = {
            "items": True
        }
    while vacancies["items"]:
        response = requests.get(
            "https://api.hh.ru/vacancies",
            params=payload)
        response.raise_for_status()
        vacancies = response.json()
        for vacancy in vacancies["items"]:
            expected_salary = predict_rub_salary_hh(vacancy)
            if expected_salary:
                vacancies_processed += 1
                salaries_sum += expected_salary
        payload["page"] += 1
    payload["page"] = 0
    vacancies_number = vacancies["found"]
    return vacancies_number, vacancies_processed, salaries_sum


def main():
    load_dotenv()
    sj_headers = {
            "X-Api-App-Id": os.environ["SJ_X_API_APP_ID"],
        }
    sj_table_data = [
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
    sj_payload = {
        "town": "Москва",
        "page": 0,
        "keyword": None
    }
    for language in languages:
        sj_payload["keyword"] = language
        sj_payload["page"] = 0
        vacancies_number, vacancies_processed, salaries_sum = get_sj_language_stat(language, sj_payload, sj_headers)
        if vacancies_processed:
            average_salary = salaries_sum // vacancies_processed
        else:
            average_salary = None
        sj_table_data.append([
            language,
            vacancies_number,
            vacancies_processed,
            average_salary])
    table = AsciiTable(sj_table_data, "Superjob Moscow")
    table.inner_heading_row_border = True
    print(table.table)
    print()
    hh_table_data = [
        [
            "Язык программирования",
            "Вакансий найдено",
            "Вакансий обработано",
            "Средняя зарплата"
            ]
        ]
    programmer_index = 96
    moscow_index = 1
    publication_period = 28
    hh_payload = {
        "professional_role": programmer_index,
        "area": moscow_index,
        "period": publication_period,
        "text": None,
        "page": 0,
        "per_page": 100
        }
    for language in languages:
        time.sleep(1)
        hh_payload["text"] = language
        hh_payload["page"] = 0
        vacancies_number, vacancies_processed, salaries_sum = get_hh_language_stat(language, hh_payload)
        if vacancies_processed:
            average_salary = salaries_sum // vacancies_processed
        else:
            average_salary = 0
        hh_table_data.append([
            language,
            vacancies_number,
            vacancies_processed,
            average_salary])
    table = AsciiTable(hh_table_data, "HeadHunter Moscow")
    table.inner_heading_row_border = True
    print(table.table)


if __name__ == "__main__":
    main()
