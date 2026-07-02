"""
main.py

Master menu. Must be run from the project root:
    cd Crime_Investigation_System
    python main.py

All four modules read/write CSVs under data/ using paths relative to the
current working directory, so this file must be launched from the project
root folder, not from inside modules/.
"""

from modules import crime_registration
from modules import evidence_suspect
from modules import crime_analysis
from modules import investigation_report


def main():
    while True:
        print("\n" + "=" * 40)
        print(" CRIME INVESTIGATION MANAGEMENT SYSTEM")
        print("=" * 40)
        print("1. Register New Case")
        print("2. Manage Evidence & Suspects")
        print("3. Crime Analysis")
        print("4. Generate Investigation Report")
        print("5. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            crime_registration.run_registration_menu()
        elif choice == "2":
            evidence_suspect.run_evidence_suspect_menu()
        elif choice == "3":
            crime_analysis.run_analysis_menu()
        elif choice == "4":
            investigation_report.run_report_menu()
        elif choice == "5":
            print("Exiting. Goodbye.")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
