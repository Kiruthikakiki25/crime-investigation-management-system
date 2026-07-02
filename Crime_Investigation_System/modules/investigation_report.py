"""
investigation_report.py
Module owner: Person 4

Responsibility: generate a final report for a given case_id by pulling data
from cases.csv, evidence.csv, and suspects.csv, then writing a summary row
to reports.csv. This is the LAST module in the chain — it depends on all
three other CSVs already having data for the case being reported on.
"""

import csv
import os
from datetime import date

DATA_DIR = "data"
CASES_FILE = os.path.join(DATA_DIR, "cases.csv")
EVIDENCE_FILE = os.path.join(DATA_DIR, "evidence.csv")
SUSPECTS_FILE = os.path.join(DATA_DIR, "suspects.csv")
REPORTS_FILE = os.path.join(DATA_DIR, "reports.csv")
REPORT_FIELDS = ["report_id", "case_id", "summary", "generated_date", "officer_id"]


def _read_csv(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _generate_report_id():
    reports = _read_csv(REPORTS_FILE)
    if not reports:
        return "R001"
    last_num = max(int(r["report_id"][1:]) for r in reports)
    return f"R{last_num + 1:03d}"


def generate_report():
    case_id = input("Enter case_id to generate report for: ").strip()
    cases = _read_csv(CASES_FILE)
    case = next((c for c in cases if c["case_id"] == case_id), None)

    if not case:
        print("No such case_id found.")
        return

    evidence = [e for e in _read_csv(EVIDENCE_FILE) if e["case_id"] == case_id]
    suspects = [s for s in _read_csv(SUSPECTS_FILE) if s["case_id"] == case_id]

    evidence_desc = ", ".join(e["description"] for e in evidence) if evidence else "None collected"
    suspect_desc = ", ".join(f"{s['name']} ({s['status']})" for s in suspects) if suspects else "None identified"

    summary = (
        f"Case: {case['title']} | Type: {case['crime_type']} | Status: {case['status']} | "
        f"Evidence: {len(evidence)} item(s) - {evidence_desc} | "
        f"Suspects: {len(suspects)} - {suspect_desc} | "
        f"Investigating Officer: {case['officer_id']}"
    )

    report_id = _generate_report_id()
    row = {
        "report_id": report_id,
        "case_id": case_id,
        "summary": summary,
        "generated_date": date.today().isoformat(),
        "officer_id": case["officer_id"],
    }

    file_exists = os.path.exists(REPORTS_FILE) and os.path.getsize(REPORTS_FILE) > 0
    with open(REPORTS_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=REPORT_FIELDS)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

    print(f"\nReport generated. Report ID: {report_id}")
    print("-" * 60)
    print(summary)
    print("-" * 60)


def list_reports():
    reports = _read_csv(REPORTS_FILE)
    if not reports:
        print("No reports generated yet.")
        return
    for r in reports:
        print(f"\n{r['report_id']} | Case: {r['case_id']} | Date: {r['generated_date']}")
        print(r["summary"])


def run_report_menu():
    while True:
        print("\n--- INVESTIGATION REPORT MENU ---")
        print("1. Generate Report for a Case")
        print("2. List All Reports")
        print("0. Back to Main Menu")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            generate_report()
        elif choice == "2":
            list_reports()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    run_report_menu()
