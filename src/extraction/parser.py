import json
import pandas as pd
import re

from config import VOL2_STAGING,TABLE_2_3_VOL2,VOL2_PROCESSED

# ---------------------------------------------------
# Rows whose first token matches these are table headers
# ---------------------------------------------------

HEADER_WORDS = {
    "2019",
    "Table",
    "Sex*",
    "Sub",
    "County",
    "Group",
    "Persons",
    "Per",
    "Total",
    "Male",
    "Female",
    "Conventional",
    "Quarters",
    "Density",
}

def load_rows():
    rows_file =(
        VOL2_STAGING
        /f"{TABLE_2_3_VOL2['output_name']}_rows.json"
    )

    with open(rows_file,encoding="utf-8")as f:
        return json.load(f)
    

def remove_headers(rows):

    cleaned = []

    for row in rows:

        tokens = row["row"]

        if not tokens:
            continue

        first = tokens[0]

        if first in HEADER_WORDS:
            continue

        if first.startswith("*"):
            continue

        if first == "Table":
            continue

        if first.isdigit() and len(tokens) == 1:
            continue

        cleaned.append(tokens)

    return cleaned


NUMBER_PATTERN = re.compile(r"^\d{1,3}(,\d{3})*$")

def merge_split_numbers(tokens):

    merged = []

    i = 0

    while i < len(tokens):

        current = tokens[i]

        # Check if there is another token
        if i + 1 < len(tokens):

            nxt = tokens[i + 1]

            # Example:
            # 1 ,208,333  -> 1,208,333
            if nxt.startswith(","):
                merged.append(current + nxt)
                i += 2
                continue

        # Default case
        merged.append(current)
        i += 1

    return merged

def merge_place_names(tokens):

    place = []
    numbers = []

    for token in tokens:

        if token == "-" or re.match(r"^[\d,]+$", token):
            numbers.append(token)
        else:
            place.append(token)

    return [" ".join(place)] + numbers   
         

def repair_first_population(tokens):

    # One-word place names
    if len(tokens) == 10 and tokens[1].isdigit():

        tokens[2] = tokens[1] + tokens[2]
        del tokens[1]

    # Two-word place names
    elif len(tokens) == 11 and tokens[2].isdigit():

        tokens[3] = tokens[2] + tokens[3]
        del tokens[2]

    return tokens 


def clean_special_cases(tokens):
    """
    Repairs KNBS extraction anomalies that cannot be solved by the generic parser.
    """
    # Rows with missing data
    if len(tokens) == 8:
        tokens.append(None)
    return tokens    

def parse_number(value):
    if value in (None, "-"):
        return None   
    return int(value.replace(",",""))

def parse_record(tokens):
    
    if len(tokens) != 9:
        print(f"Skipped ({len(tokens)}fields):{tokens}")
        return None
    
    return {
        "sub_county": tokens[0],
        "total_population": parse_number(tokens[1]),
        "male": parse_number(tokens[2]),
        "female": parse_number(tokens[3]),
        "households": parse_number(tokens[4]),
        "conventional_households": parse_number(tokens[5]),
        "group_quarters": parse_number(tokens[6]),
        "land_area_sq_km": parse_number(tokens[7]),
        "population_density": parse_number(tokens[8]),
    }

def main():

    rows = load_rows()

    rows = remove_headers(rows)

    records = []

    for row in rows:

        cleaned = merge_split_numbers(row)
        cleaned = merge_place_names(cleaned)
        cleaned = repair_first_population(cleaned)
        cleaned = clean_special_cases(cleaned)
        record = parse_record(cleaned)

        if record:
            records.append(record)

    df = pd.DataFrame(records)

    output_folder = VOL2_PROCESSED

    output_folder.mkdir(parents=True, exist_ok=True)

    output_file = (
        output_folder
        / f"{TABLE_2_3_VOL2["output_name"]}.csv"
    )

    df.to_csv(output_file, index=False)

    print(df.head(20))
    print(df.shape)
    print(f"\nSaved cleaned dataset to:\n{output_file}")

if __name__ == "__main__":
    main()

