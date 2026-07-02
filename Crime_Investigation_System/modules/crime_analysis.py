"""
crime_analysis.py

Module owner: Person 3

Role in the system:
    This module is READ-ONLY. It never writes to any CSV. It reads data that
    crime_registration.py and evidence_suspect.py have already written
    (cases.csv, evidence.csv, suspects.csv) and produces statistics.

    It must run AFTER cases/evidence/suspects exist. If the CSVs are empty,
    every function here will report "no data" instead of crashing.

Data contract (must match what P1 and P2 write):
    cases.csv    : case_id,title,crime_type,date_reported,location,status,officer_id
    evidence.csv : evidence_id,case_id,description,evidence_type,date_collected
    suspects.csv : suspect_id,case_id,name,age,gender,status

If any teammate changes a column name, the constants below (CASES_FILE,
field names) are the single place to fix it.
"""

import csv
import os
from collections import Counter, defaultdict

# ---------------------------------------------------------------------------
# File locations — relative to project root, not to this file's folder.
# main.py must be run from Crime_Investigation_System/ for these paths to work.
# ---------------------------------------------------------------------------
DATA_DIR = "data"
CASES_FILE = os.path.join(DATA_DIR, "cases.csv")
EVIDENCE_FILE = os.path.join(DATA_DIR, "evidence.csv")
SUSPECTS_FILE = os.path.join(DATA_DIR, "suspects.csv")
OFFICERS_FILE = os.path.join(DATA_DIR, "officers.csv")


# ---------------------------------------------------------------------------
# Shared read helper. Every analysis function depends on this. If the file
# doesn't exist yet (a teammate hasn't run their module / created the CSV),
# we return an empty list instead of crashing the whole program.
# ---------------------------------------------------------------------------
def _read_csv(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [row for row in reader]


def _load_all():
    cases = _read_csv(CASES_FILE)
    evidence = _read_csv(EVIDENCE_FILE)
    suspects = _read_csv(SUSPECTS_FILE)
    officers = _read_csv(OFFICERS_FILE)
    return cases, evidence, suspects, officers


# ---------------------------------------------------------------------------
# Individual analysis functions. Each one is independent — if one CSV is
# missing a column or empty, only that report is affected, not the others.
# ---------------------------------------------------------------------------

def crime_type_frequency(cases):
    """How many cases per crime_type. Answers: what crime is most common."""
    counts = Counter(c["crime_type"] for c in cases if c.get("crime_type"))
    return counts.most_common()


def case_status_breakdown(cases):
    """Open vs Closed count. Answers: how much of the workload is unresolved."""
    return Counter(c["status"] for c in cases if c.get("status"))


def officer_workload(cases, officers):
    """Case count per officer. Answers: who is overloaded."""
    counts = Counter(c["officer_id"] for c in cases if c.get("officer_id"))
    officer_names = {o["officer_id"]: o["name"] for o in officers}
    result = []
    for officer_id, count in counts.most_common():
        name = officer_names.get(officer_id, "Unknown Officer")
        result.append((officer_id, name, count))
    return result


def monthly_case_trend(cases):
    """Cases per YYYY-MM. Answers: is crime rising or falling month to month."""
    counts = Counter()
    for c in cases:
        date_str = c.get("date_reported", "")
        if len(date_str) >= 7:
            year_month = date_str[:7]  # "2026-03" from "2026-03-15"
            counts[year_month] += 1
    return sorted(counts.items())


def evidence_type_distribution(evidence):
    """Digital vs Physical vs other evidence counts. Answers: what kind of
    evidence this department collects most — relevant for resourcing
    (e.g. more digital forensics capacity needed)."""
    return Counter(e["evidence_type"] for e in evidence if e.get("evidence_type"))


def evidence_count_per_case(evidence):
    """How many evidence items each case has. Answers: which cases are
    evidence-poor and may need more investigation."""
    counts = Counter(e["case_id"] for e in evidence if e.get("case_id"))
    return counts.most_common()


def repeat_suspects(suspects):
    """Suspects (by name) appearing in more than one case. Answers: who is
    a repeat offender across cases. NOTE: matched by name only, since there
    is no separate suspects-master file with a stable suspect identity.
    Two different people with the same name will be wrongly merged — this
    is a known limitation worth mentioning if asked in viva."""
    case_lists = defaultdict(set)
    for s in suspects:
        name = s.get("name", "").strip()
        case_id = s.get("case_id", "").strip()
        if name and case_id and name.lower() != "unknown":
            case_lists[name].add(case_id)
    repeats = [(name, sorted(cases)) for name, cases in case_lists.items() if len(cases) > 1]
    repeats.sort(key=lambda x: len(x[1]), reverse=True)
    return repeats


def suspect_status_breakdown(suspects):
    """Arrested vs Wanted vs Cleared. Answers: arrest rate."""
    return Counter(s["status"] for s in suspects if s.get("status"))


# ---------------------------------------------------------------------------
# Console output formatting — kept separate from the calculation functions
# above, so if P4 wants to reuse the raw numbers in investigation_report.py
# instead of printed text, they can call e.g. crime_type_frequency(cases)
# directly without touching the print logic.
# ---------------------------------------------------------------------------

def _print_header(title):
    print("\n" + "=" * 50)
    print(title)
    print("=" * 50)


def show_crime_type_frequency(cases):
    _print_header("CRIME TYPE FREQUENCY")
    data = crime_type_frequency(cases)
    if not data:
        print("No case data available.")
        return
    for crime_type, count in data:
        print(f"{crime_type:<20}{count}")


def show_case_status_breakdown(cases):
    _print_header("CASE STATUS BREAKDOWN")
    data = case_status_breakdown(cases)
    if not data:
        print("No case data available.")
        return
    total = sum(data.values())
    for status, count in data.items():
        pct = (count / total) * 100
        print(f"{status:<15}{count:<5}({pct:.1f}%)")


def show_officer_workload(cases, officers):
    _print_header("OFFICER WORKLOAD")
    data = officer_workload(cases, officers)
    if not data:
        print("No case data available.")
        return
    for officer_id, name, count in data:
        print(f"{officer_id:<8}{name:<25}{count} case(s)")


def show_monthly_trend(cases):
    _print_header("MONTHLY CASE TREND")
    data = monthly_case_trend(cases)
    if not data:
        print("No case data available.")
        return
    for month, count in data:
        bar = "#" * count
        print(f"{month}  {bar} ({count})")


def show_evidence_type_distribution(evidence):
    _print_header("EVIDENCE TYPE DISTRIBUTION")
    data = evidence_type_distribution(evidence)
    if not data:
        print("No evidence data available.")
        return
    for etype, count in data.items():
        print(f"{etype:<15}{count}")


def show_evidence_count_per_case(evidence):
    _print_header("EVIDENCE COUNT PER CASE")
    data = evidence_count_per_case(evidence)
    if not data:
        print("No evidence data available.")
        return
    for case_id, count in data:
        print(f"{case_id:<10}{count} item(s)")


def show_repeat_suspects(suspects):
    _print_header("REPEAT SUSPECTS (across multiple cases)")
    data = repeat_suspects(suspects)
    if not data:
        print("No repeat suspects found.")
        return
    for name, case_ids in data:
        print(f"{name:<20}-> cases: {', '.join(case_ids)}")


def show_suspect_status_breakdown(suspects):
    _print_header("SUSPECT STATUS BREAKDOWN")
    data = suspect_status_breakdown(suspects)
    if not data:
        print("No suspect data available.")
        return
    for status, count in data.items():
        print(f"{status:<15}{count}")


# ---------------------------------------------------------------------------
# Entry point called from main.py's menu.
#   from modules import crime_analysis
#   crime_analysis.run_analysis_menu()
# ---------------------------------------------------------------------------

def run_analysis_menu():
    cases, evidence, suspects, officers = _load_all()

    if not cases:
        print("\nNo cases registered yet. Register a case first (Menu Option 1).")
        return

    while True:
        print("\n--- CRIME ANALYSIS MENU ---")
        print("1. Crime Type Frequency")
        print("2. Case Status Breakdown")
        print("3. Officer Workload")
        print("4. Monthly Case Trend")
        print("5. Evidence Type Distribution")
        print("6. Evidence Count per Case")
        print("7. Repeat Suspects Across Cases")
        print("8. Suspect Status Breakdown")
        print("9. Run All Reports")
        print("0. Back to Main Menu")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            show_crime_type_frequency(cases)
        elif choice == "2":
            show_case_status_breakdown(cases)
        elif choice == "3":
            show_officer_workload(cases, officers)
        elif choice == "4":
            show_monthly_trend(cases)
        elif choice == "5":
            show_evidence_type_distribution(evidence)
        elif choice == "6":
            show_evidence_count_per_case(evidence)
        elif choice == "7":
            show_repeat_suspects(suspects)
        elif choice == "8":
            show_suspect_status_breakdown(suspects)
        elif choice == "9":
            show_crime_type_frequency(cases)
            show_case_status_breakdown(cases)
            show_officer_workload(cases, officers)
            show_monthly_trend(cases)
            show_evidence_type_distribution(evidence)
            show_evidence_count_per_case(evidence)
            show_repeat_suspects(suspects)
            show_suspect_status_breakdown(suspects)
        elif choice == "0":
            break
        else:
            print("Invalid choice. Try again.")


# Allows testing this module directly: python modules/crime_analysis.py
# (run from the project root so the data/ relative path resolves correctly)
if __name__ == "__main__":
    run_analysis_menu()
