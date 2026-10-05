import csv

with open('CustodianOfficers.csv', 'r', encoding='cp1252') as f:
    rows = list(csv.reader(f))

header = rows[0]
posted_idx = next(i for i, h in enumerate(header) if 'POSTED' in h.upper())
print(f"Column index: {posted_idx}, Header: '{header[posted_idx]}'")

changed = 0
for row in rows[1:]:
    if len(row) > posted_idx and '|' in row[posted_idx]:
        row[posted_idx] = row[posted_idx][row[posted_idx].rindex('|') + 1:].strip()
        changed += 1

print(f"Rows changed: {changed}")

with open('CustodianOfficers.csv', 'w', encoding='cp1252', newline='') as f:
    writer = csv.writer(f, lineterminator='\r\n')
    writer.writerows(rows)

print("File saved. Verifying first 5 rows:")
with open('CustodianOfficers.csv', 'r', encoding='cp1252') as f:
    rows2 = list(csv.reader(f))
for r in rows2[1:6]:
    print(f"  '{r[posted_idx]}'")
