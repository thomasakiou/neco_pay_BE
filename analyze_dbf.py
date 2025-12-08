from dbfread import DBF
import os

dbf_path = "staff.DBF"

if not os.path.exists(dbf_path):
    print(f"File not found: {dbf_path}")
else:
    table = DBF(dbf_path)
    with open("dbf_schema.txt", "w") as f:
        f.write("Fields:\n")
        for field in table.fields:
            f.write(f"Name: {field.name}, Type: {field.type}, Length: {field.length}\n")
    print("Schema written to dbf_schema.txt")
