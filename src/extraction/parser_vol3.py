import json

from config import VOL3_STAGING, TABLE_2_3_VOL3

HEADER_WORDS = {
    "2019",
    "Table",
    "Age",
    "Male",
    "Female",
    "Total",
    "County",
    "Sub-",
    "County",
    "Sub",
    "Sex*",
}

def load_rows():
    rows_file = (
        VOL3_STAGING
        /f"{TABLE_2_3_VOL3['output_name']}_rows.json"
    )

    with open(rows_file,encoding="utf-8") as f:
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

        cleaned.append(tokens)

    return cleaned

def expected_age_labels():
    labels = ["Total"]

    for start in range(0,100,5):
        #Individual ages
        for age in range(start,start + 5):
            labels.append(str(age))

        #Five-year age group
        labels.append(f"{start}-{start+4}")
    
    labels.append("100+")
    labels.append("Not Stated")

    return labels

def normalize_rows(rows):
    normalized = []

    for tokens in rows:
        #county/sub-county names
        if len(tokens) == 1:
            normalized.append(tokens)
            continue
        
        #Repair age labels
        repaired = []
        i = 0
        while i < len(tokens):
            #0 - 4 -> 0-4
            if(
                i + 2 < len(tokens)
                and tokens[i].isdigit()
                and tokens[i + 1] == "-"
                and tokens[i +2].isdigit()
            ):
                repaired.append(f"{tokens[i]}-{tokens[i+2]}")
                i += 3
                continue

            #10 -14 -> 10-14
            if(
                i + 1 < len(tokens)
                and tokens[i].isdigit()
                and tokens[i + 1].startswith("-")
            ):
                repaired.append(tokens[i] + tokens[i+1])
                i += 2
                continue

            #not stated
            if(
                i + 1 < len(tokens)
                and tokens[i] == "Not"
                and tokens[i+1] == "Stated"
            ):
                repaired.append("Not Stated")
                i += 2
                continue

            repaired.append(tokens[i])
            i += 1
        
        normalized.append(repaired)

    return normalized

def split_embedded_rows(rows):
    """
    Split rows where OCR merged multiple age records into one row.
    """
    expected = set(expected_age_labels())

    split_rows = []
    
    for tokens in rows:
        #county/subcounty names
        if len(tokens) == 1:
            split_rows.append(tokens)
            continue

        current = []

        i = 0

        while i < len(tokens):
            token = tokens[i]

            #start of a new age row
            if token in expected:
                #save previous row if it exists
                if current:
                    split_rows.append(current)

                current = [token]  

            else:
                current.append(token)

            i += 1

        if current:
            split_rows.append(current)              
    
    return split_rows

def reconstruct_rows(rows):
    reconstructed = []

    current_row = None

    expected = expected_age_labels()
    expected_set = set(expected)

    for tokens in rows:
        #COUNTY/SUBCOUNTY NAMES
        if len(tokens) == 1:
            if current_row:
                reconstructed.append(current_row)
                current_row = None

            reconstructed.append(tokens)
            continue

        first = tokens[0]

        # NEW AGE ROW
        if first in expected_set:

            if current_row:
                reconstructed.append(current_row)

            current_row = tokens

        else:
            #OCR continuation
            if current_row:
                current_row.extend(tokens)

    if current_row:
        reconstructed.append(current_row)

    return reconstructed                        

    
def main():

    rows = load_rows()

    rows = remove_headers(rows)

    rows = normalize_rows(rows)
    rows = split_embedded_rows(rows)
    rows = reconstruct_rows(rows)

    for row in rows[:100]:
        print(row) 
       

if __name__ == "__main__":
    main()