# Подсчет зарплаты для программиста.

Данный проект может быть использован подсчета средней зарплаты программиста на разных языках программирования на двух сайтах: Superjob, Headhunter.

### Как установить

Для отправления запроса к Superjob необходим заголовок X-Api-App-Id. Для того, чтобы его задать нужно выполнить следующие шаги: Создать файл `.env`, в нем переменную `SJ_X_API_APP_ID`, а в значение записать свой X-Api-App-Id для Superjob.

Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```

### Пример запуска

```
>>>python main.py

+Superjob Moscow--------+------------------+---------------------+------------------+
| Язык программирования | Вакансий найдено | Вакансий обработано | Средняя зарплата |
+-----------------------+------------------+---------------------+------------------+
| JavaScript            | 7                | 3                   | 114000.0         |
| Java                  | 3                | 1                   | 120000.0         |
| Python                | 8                | 6                   | 120666.0         |
| Ruby                  | 0                | 0                   | None             |
| PHP                   | 7                | 5                   | 130000.0         |
| C++                   | 6                | 5                   | 160800.0         |
| C#                    | 3                | 3                   | 175000.0         |
| TypeScript            | 5                | 2                   | 96000.0          |
+-----------------------+------------------+---------------------+------------------+

+HeadHunter Moscow------+------------------+---------------------+------------------+
| Язык программирования | Вакансий найдено | Вакансий обработано | Средняя зарплата |
+-----------------------+------------------+---------------------+------------------+
| JavaScript            | 1496             | 586                 | 173741.0         |
| Java                  | 866              | 174                 | 205349.0         |
| Python                | 1283             | 302                 | 207024.0         |
| Ruby                  | 48               | 18                  | 241222.0         |
| PHP                   | 681              | 313                 | 183153.0         |
| C++                   | 928              | 247                 | 210891.0         |
| C#                    | 616              | 164                 | 218237.0         |
| TypeScript            | 715              | 248                 | 178911.0         |
+-----------------------+------------------+---------------------+------------------+
```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).