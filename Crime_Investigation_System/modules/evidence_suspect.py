"""
evidence_suspect.py
Module owner: Person 2

Responsibility: add evidence linked to a case_id, add suspects linked to a
case_id. Writes to data/evidence.csv and data/suspects.csv. Depends on
crime_registration.py already having created the case_id being referenced —
this module validates that case_id exists in cases.csv before accepting it.
"""

import csv
import os

DATA_DIR = "data"
CASES_FILE = os.path.join(DATA_DIR, "cases.csv")
EVIDENCE_FILE = os.path.join(DATA_DIR, "evidence.csv")
SUSPECTS_FILE = os.path.join(DATA_DIR, "suspects.csv")

EVIDENCE_FIELDS = ["evidence_id", "case_id", "description", "evidence_type", "date_collected"]
SUSPECT_FIELDS = ["suspect_id", "case_id", "name", "age", "gender", "status"]


def _read_csv(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _append_row(filepath, fieldnames, row):
    file_exists = os.path.exists(filepath) and os.path.getsize(filepath) > 0
    with open(filepath, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def _case_exists(case_id):
    cases = _read_csv(CASES_FILE)
    return any(c["case_id"] == case_id for c in cases)


def _generate_id(filepath, prefix):
    rows = _read_csv(filepath)
    id_field = "evidence_id" if prefix == "E" else "suspect_id"
    if not rows:
        return f"{prefix}001"
    last_num = max(int(r[id_field][1:]) for r in rows)
    return f"{prefix}{last_num + 1:03d}"


def add_evidence():
    case_id = input("Enter case_id this evidence belongs to: ").strip()
    if not _case_exists(case_id):
        print("No such case_id found in cases.csv. Register the case first.")
        return

    evidence_id = _generate_id(EVIDENCE_FILE, "E")
    description = input("Evidence description: ").strip()
    evidence_type = input("Evidence type (Digital/Physical): ").strip()
    date_collected = input("Date collected (YYYY-MM-DD): ").strip()

    row = {
        "evidence_id": evidence_id,
        "case_id": case_id,
        "description": description,
        "evidence_type": evidence_type,
        "date_collected": date_collected,
    }
    _append_row(EVIDENCE_FILE, EVIDENCE_FIELDS, row)
    print(f"Evidence added. Evidence ID: {evidence_id}")


def add_suspect():
    case_id = input("Enter case_id this suspect belongs to: ").strip()
    if not _case_exists(case_id):
        print("No such case_id found in cases.csv. Register the case first.")
        return

    suspect_id = _generate_id(SUSPECTS_FILE, "S")
    name = input("Suspect name: ").strip()
    age = input("Age: ").strip()
    gender = input("Gender (M/F/U): ").strip()
    status = input("Status (Arrested/Wanted/Cleared): ").strip()

    row = {
        "suspect_id": suspect_id,
        "case_id": case_id,
        "name": name,
        "age": age,
        "gender": gender,
        "status": status,
    }
    _append_row(SUSPECTS_FILE, SUSPECT_FIELDS, row)
    print(f"Suspect added. Suspect ID: {suspect_id}")


def list_evidence_for_case():
    case_id = input("Enter case_id: ").strip()
    evidence = [e for e in _read_csv(EVIDENCE_FILE) if e["case_id"] == case_id]
    if not evidence:
        print("No evidence found for this case.")
        return
    for e in evidence:
        print(f"{e['evidence_id']:<8}{e['evidence_type']:<12}{e['description']}")


def list_suspects_for_case():
    case_id = input("Enter case_id: ").strip()
    suspects = [s for s in _read_csv(SUSPECTS_FILE) if s["case_id"] == case_id]
    if not suspects:
        print("No suspects found for this case.")
        return
    for s in suspects:
        print(f"{s['suspect_id']:<8}{s['name']:<20}{s['status']}")


def run_evidence_suspect_menu():
    while True:
        print("\n--- EVIDENCE & SUSPECT MENU ---")
        print("1. Add Evidence")
        print("2. Add Suspect")
        print("3. List Evidence for a Case")
        print("4. List Suspects for a Case")
        print("0. Back to Main Menu")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            add_evidence()
        elif choice == "2":
            add_suspect()
        elif choice == "3":
            list_evidence_for_case()
        elif choice == "4":
            list_suspects_for_case()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    run_evidence_suspect_menu()
