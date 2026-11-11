"""Практична робота №5–6, завдання 2, варіант 5: пошук мінімального та максимального ВВП на душу населення."""

import csv
from decimal import Decimal, InvalidOperation
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
INPUT = ROOT / "output" / "usa_gdp_per_capita_1991_2019.csv"
RESULT = ROOT / "output" / "usa_gdp_per_capita_min_max.csv"
EXPECTED_HEADER = {"country", "country_code", "year", "gdp_per_capita_current_usd"}


def read_csv_records(path):
    """Зчитування вихідного CSV із перевіркою полів і значень."""
    records = []
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        if not reader.fieldnames or not EXPECTED_HEADER.issubset(reader.fieldnames):
            raise ValueError("CSV-файл не містить необхідних стовпців.")
        for row in reader:
            if row["country_code"] != "USA":
                continue
            year = int(row["year"])
            if not 1991 <= year <= 2019:
                continue
            value = Decimal(row["gdp_per_capita_current_usd"])
            if not value.is_finite():
                raise ValueError("Значення показника має бути скінченним числом.")
            records.append({"country": row["country"], "year": year, "value": value})
    if len(records) != 29 or {entry["year"] for entry in records} != set(range(1991, 2020)):
        raise ValueError("У файлі очікуються 29 різних років: 1991–2019.")
    return records


def calculate_extrema(records):
    return min(records, key=lambda row: row["value"]), max(records, key=lambda row: row["value"])


def save_results(low, high, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["extremum", "country", "year", "gdp_per_capita_current_usd"])
        for label, row in (("minimum", low), ("maximum", high)):
            writer.writerow([label, row["country"], row["year"], str(row["value"])])


def main():
    try:
        records = read_csv_records(INPUT)
        minimum, maximum = calculate_extrema(records)
        save_results(minimum, maximum, RESULT)
        print("ПРАКТИЧНА РОБОТА №5–6 — ЗАВДАННЯ 2, ВАРІАНТ 5")
        print("Показник: GDP per capita (current US$), США, 1991–2019 рр.")
        print(f"Прочитано записів: {len(records)}")
        print(f"Мінімум: {minimum['year']} р., {minimum['value']:.2f} дол. США")
        print(f"Максимум: {maximum['year']} р., {maximum['value']:.2f} дол. США")
        print(f"Результат збережено: {RESULT.relative_to(ROOT)}")
        print("\n===== ВМІСТ РЕЗУЛЬТУЮЧОГО CSV =====")
        with RESULT.open("r", encoding="utf-8-sig") as file:
            print(file.read().rstrip())
    except (OSError, ValueError, InvalidOperation) as error:
        print(f"Помилка пошуку у CSV-файлі: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
