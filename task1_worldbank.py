"""Практична робота №5–6, завдання 1, варіант 5: World Bank API -> JSON -> CSV."""

import argparse
import csv
import json
from pathlib import Path
import sys

import requests

COUNTRY = "USA"
INDICATOR = "NY.GDP.PCAP.CD"  # GDP per capita (current US$)
START_YEAR = 1991
END_YEAR = 2019
API_URL = f"https://api.worldbank.org/v2/country/{COUNTRY}/indicator/{INDICATOR}"
ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "output"
JSON_FILE = OUTPUT / "usa_gdp_per_capita_1991_2019.json"
CSV_FILE = OUTPUT / "usa_gdp_per_capita_1991_2019.csv"
REFERENCE = ROOT / "data" / "worldbank_usa_gdp_per_capita_1991_2019_reference.json"


def fetch_data(offline=False):
    """Отримання відповіді API або читання збереженого контрольного набору."""
    if offline:
        with REFERENCE.open("r", encoding="utf-8") as file:
            result = json.load(file)
        print("Режим: перевірка на збережених даних Світового банку.")
        return result
    response = requests.get(
        API_URL,
        params={"date": f"{START_YEAR}:{END_YEAR}", "format": "json", "per_page": 500},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def validate_and_convert(payload):
    """Перевірка структури відповіді та формування 29 рядків для CSV."""
    if not isinstance(payload, list) or len(payload) != 2 or not isinstance(payload[1], list):
        raise ValueError("API повернуло некоректну структуру JSON.")
    if isinstance(payload[0], dict) and payload[0].get("message"):
        raise ValueError(f"Помилка API: {payload[0]['message']}")

    csv_rows = []
    for entry in payload[1]:
        if not isinstance(entry, dict):
            continue
        if entry.get("countryiso3code") != COUNTRY:
            continue
        if entry.get("indicator", {}).get("id") != INDICATOR:
            continue
        year_text = str(entry.get("date", ""))
        if not year_text.isdigit():
            continue
        year = int(year_text)
        if START_YEAR <= year <= END_YEAR:
            value = entry.get("value")
            if value is None:
                raise ValueError(f"Відсутнє значення показника за {year} рік.")
            csv_rows.append({
                "country": entry["country"]["value"],
                "country_code": COUNTRY,
                "year": year,
                "gdp_per_capita_current_usd": value,
            })
    csv_rows.sort(key=lambda row: row["year"])
    expected = list(range(START_YEAR, END_YEAR + 1))
    if [row["year"] for row in csv_rows] != expected:
        raise ValueError("Відповідь не містить усіх 29 років (1991–2019) без повторів.")
    return csv_rows


def save_data(payload, rows):
    OUTPUT.mkdir(parents=True, exist_ok=True)
    with JSON_FILE.open("w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=False, indent=2)
    fieldnames = ["country", "country_code", "year", "gdp_per_capita_current_usd"]
    with CSV_FILE.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def show_files():
    """За вимогою методички показати повний вміст обох створених файлів."""
    for label, file_path in (("JSON", JSON_FILE), ("CSV", CSV_FILE)):
        print(f"\n===== ВМІСТ {label}: {file_path.name} =====")
        with file_path.open("r", encoding="utf-8-sig") as file:
            print(file.read().rstrip())


def main():
    parser = argparse.ArgumentParser(description="Дані ВВП на душу населення США за 1991–2019 роки")
    parser.add_argument("--offline", action="store_true", help="Перевірка на контрольній копії даних без HTTP")
    args = parser.parse_args()
    try:
        payload = fetch_data(offline=args.offline)
        rows = validate_and_convert(payload)
        save_data(payload, rows)
        print(f"Отримано записів: {len(rows)}")
        print(f"JSON: {JSON_FILE.relative_to(ROOT)}")
        print(f"CSV:  {CSV_FILE.relative_to(ROOT)}")
        show_files()
        print("\nЗавдання 1 практичної роботи №5–6 виконано успішно.")
    except (requests.RequestException, OSError, ValueError, json.JSONDecodeError) as error:
        print(f"Помилка оброблення даних: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
