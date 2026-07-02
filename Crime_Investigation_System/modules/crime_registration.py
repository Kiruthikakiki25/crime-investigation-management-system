"""
crime_registration.py
Module owner: Person 1

Responsibility: register new cases, assign case_id, update case status,
list/search cases. Writes to data/cases.csv. This is the FIRST module in
the chain — every other module depends on case_id values created here.
"""

import csv
import os

DATA_DIR = "data"
CASES_FILE = os.path.join(DATA_DIR, "cases.csv")
FIELDNAMES = ["case_id", "title", "crime_type", "date_reported", "location", "status", "officer_id"]


def _read_all_cases():
    if not os.path.exists(CASES_FILE):
        return []
    with open(CASES_FILE, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _write_all_cases(cases):
    with open(CASES_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(cases)


def _generate_case_id(cases):
    """Locked format: C001, C002, C003... Every module agrees on this format."""
    if not cases:
        return "C001"
    last_num = max(int(c["case_id"][1:]) for c in cases)
    return f"C{last_num + 1:03d}"


def register_case():
    cases = _read_all_cases()
    case_id = _generate_case_id(cases)

    print(f"\nRegistering new case (ID will be: {case_id})")
    title = input("Title: ").strip()
    crime_type = input("Crime Type (e.g. Robbery/Theft/Assault/Cybercrime): ").strip()
    date_reported = input("Date Reported (YYYY-MM-DD): ").strip()
    location = input("Location: ").strip()
    officer_id = input("Assigned Officer ID (e.g. O01): ").strip()

    new_case = {
        "case_id": case_id,
        "title": title,
        "crime_type": crime_type,
        "date_reported": date_reported,
        "location": location,
        "status": "Open",
        "officer_id": officer_id,
    }

    cases.append(new_case)
    _write_all_cases(cases)
    print(f"Case registered successfully. Case ID: {case_id}")
    return case_id


def list_cases():
    cases = _read_all_cases()
    if not cases:
        print("\nNo cases registered yet.")
        return
    print(f"\n{'ID':<8}{'Title':<28}{'Type':<14}{'Status':<10}{'Officer':<8}")
    print("-" * 68)
    for c in cases:
        print(f"{c['case_id']:<8}{c['title'][:26]:<28}{c['crime_type']:<14}{c['status']:<10}{c['officer_id']:<8}")


def search_case():
    case_id = input("Enter case_id to search: ").strip()
    cases = _read_all_cases()
    for c in cases:
        if c["case_id"] == case_id:
            print(f"\nCase ID: {c['case_id']}")
            print(f"Title: {c['title']}")
            print(f"Type: {c['crime_type']}")
            print(f"Date Reported: {c['date_reported']}")
            print(f"Location: {c['location']}")
            print(f"Status: {c['status']}")
            print(f"Officer ID: {c['officer_id']}")
            return
    print("Case not found.")


def update_case_status():
    case_id = input("Enter case_id to update: ").strip()
    cases = _read_all_cases()
    for c in cases:
        if c["case_id"] == case_id:
            new_status = input("New status (Open/Closed): ").strip()
            c["status"] = new_status
            _write_all_cases(cases)
            print("Status updated.")
            return
    print("Case not found.")


def run_registration_menu():
    while True:
        print("\n--- CRIME REGISTRATION MENU ---")
        print("1. Register New Case")
        print("2. List All Cases")
        print("3. Search Case by ID")
        print("4. Update Case Status")
        print("0. Back to Main Menu")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            register_case()
        elif choice == "2":
            list_cases()
        elif choice == "3":
            search_case()
        elif choice == "4":
            update_case_status()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    run_registration_menu()
