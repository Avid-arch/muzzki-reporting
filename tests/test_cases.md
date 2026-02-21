Test Case 1 — Duplicate detection
Input: system_a.csv contains two rows with id=4
Expected: duplicates_a CSV contains both rows for id=4

Test Case 2 — Missing values detection
Input: system_a.csv contains blank email for id=3
Expected: missing_a CSV contains row with id=3

Test Case 3 — Record mismatch
Input: system_a amount for id=2 = 200; system_b amount for id=2 = 250
Expected: mismatches CSV lists id=2 with system_a and system_b values

Test Case 4 — Only-in-system detection
Input: id=5 exists only in system_b
Expected: only_in_b CSV lists id=5