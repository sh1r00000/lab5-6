# Практична робота №5–6 — Програмування мовою Python

**Варіант №5.** Студент: Мовсесян Ніколай Геннадійович, група КН-52/2.

## Умови

- **ПР №5.** Отримати з API Світового банку показник **GDP per capita (current US$)** для **США за 1991–2019 роки**. Зберегти відповідь у JSON, перетворити дані на CSV та вивести вміст обох файлів на екран.
- **ПР №6.** У створеному CSV знайти мінімальне та максимальне значення показника й зберегти їх у новому CSV.

Використано показник `NY.GDP.PCAP.CD`, код країни `USA`, 29 років (1991–2019).

## Запуск

Потрібні Python 3.9+ та бібліотека requests:

```bash
python -m pip install -r requirements.txt
python task1_worldbank.py
python task2_csv_extrema.py
```

Якщо немає доступу до інтернету, можна перевірити програму на локально збереженому контрольному наборі **тих самих значень офіційного API**:

```bash
python task1_worldbank.py --offline
python task2_csv_extrema.py
```

Режим `--offline` чітко повідомляє, що використано збережений набір, а не виконувався HTTP-запит. За звичайного запуску HTTP-запит виконується через `requests.get(...)` до API Світового банку.

## Файли

- `task1_worldbank.py` — завдання ПР №5;
- `task2_csv_extrema.py` — завдання ПР №6;
- `data/worldbank_usa_gdp_per_capita_1991_2019_reference.json` — збережений контрольний набір, сформований зі значень офіційного API (дата перевірки 11.11.2026);
- `output/usa_gdp_per_capita_1991_2019.json` — JSON з 29 записами;
- `output/usa_gdp_per_capita_1991_2019.csv` — CSV з 29 записами;
- `output/usa_gdp_per_capita_min_max.csv` — мінімум і максимум;
- `results/` — журнали запуску та тести;
- `assets/` — знімки фактичних консольних виводів;
- `test_programs.py` — автоматизовані перевірки.

**Мінімум:** 1991 — 24 342,26 дол. США. **Максимум:** 2019 — 65 227,96 дол. США.

## Джерела

1. World Bank Open Data: https://data.worldbank.org/indicator/NY.GDP.PCAP.CD?locations=US
2. World Bank API: https://api.worldbank.org/v2/country/USA/indicator/NY.GDP.PCAP.CD?date=1991:2019&format=json&per_page=500
3. API документація: https://datahelpdesk.worldbank.org/knowledgebase/articles/898581-api-basic-call-structures

## Публікація на GitHub

Створіть новий **публічний** репозиторій, завантажте файли з архіву та скопіюйте URL репозиторію. Після публікації додайте в PDF-звіт посилання на репозиторій і на кожен із файлів `task1_worldbank.py`, `task2_csv_extrema.py`. Зараз реальна адреса нового репозиторію ще не вказана.
