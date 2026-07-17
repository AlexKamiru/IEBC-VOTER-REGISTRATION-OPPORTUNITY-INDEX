import json

from config import KNBS_STAGING,TABLE_2_3

rows_file = (
    KNBS_STAGING
    /"volume_ii"
    /f"{TABLE_2_3['output_name']}_rows.json"
)

with open(rows_file, encoding="utf-8") as f:
    rows = json.load(f)

print(f"Total rows:{len(rows)}\n")

for i, row in enumerate(rows[:30], start=1):
    print(f"Row {i}")
    print(f"Page: {row['page']}")
    print(f"Top : {row['top']}")
    print(row["row"])
    print("-" * 80)