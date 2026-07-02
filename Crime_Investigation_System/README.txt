Crime Investigation Management System
======================================

HOW TO RUN
-----------
1. Open a terminal in this folder (Crime_Investigation_System/)
2. Run: python main.py
   (Do NOT run files from inside modules/ directly during normal use -
   main.py must be the entry point so relative paths to data/ resolve.)

FLOW (must be followed in this order for the demo to make sense)
-------------------------------------------------------------------
1. Register New Case        -> creates a case_id (C001, C002...) in cases.csv
2. Manage Evidence & Suspects -> attach evidence/suspects to an existing case_id
3. Crime Analysis            -> read-only statistics across all registered data
4. Generate Investigation Report -> final report per case, written to reports.csv

DATA CONTRACT (do not change column names without updating all 4 modules)
---------------------------------------------------------------------------
cases.csv     : case_id,title,crime_type,date_reported,location,status,officer_id
evidence.csv  : evidence_id,case_id,description,evidence_type,date_collected
suspects.csv  : suspect_id,case_id,name,age,gender,status
officers.csv  : officer_id,name,rank,station
reports.csv   : report_id,case_id,summary,generated_date,officer_id

case_id format is locked as C001, C002, C003... (3-digit zero-padded).
evidence_id is E001, E002... ; suspect_id is S001, S002... ; report_id is R001, R002...

MODULE OWNERS
-------------
P1 - crime_registration.py   (case CRUD)
P2 - evidence_suspect.py     (evidence + suspect CRUD, linked to case_id)
P3 - crime_analysis.py       (read-only statistics)
P4 - investigation_report.py + main.py (report generation + menu integration)
