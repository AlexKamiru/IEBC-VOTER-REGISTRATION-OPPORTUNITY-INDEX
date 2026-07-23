import json
from collections import defaultdict

from config import (
    VOL3_STAGING,
    TABLE_2_3_VOL3,
)

# -------------------------------------------------------
# Helpers
# -------------------------------------------------------

def load_words():
    input_file = (
        VOL3_STAGING
        /f"{TABLE_2_3_VOL3['output_name']}_words.json"
    )

    with open(input_file,encoding="utf-8") as f:
        return json.load(f)

# -------------------------------------------------------
# Find page split (LEFT vs RIGHT)
#priority:
#    1. Two "age" headers
#    2. Fixed split from config
#    3. Largest horizontal gap
# -------------------------------------------------------

def compute_page_splits(words):
    """
    Determine the split using the table headers.

    expected header:
    Age Male Female Total   Age Male Female Total
    """

    pages = defaultdict(list)

    for word in words:
        pages[word["page"]].append(word)

    splits = {}

    for page, page_words in sorted(pages.items()):

        # ----------------------------------------
        # Find all header words
        # ----------------------------------------
        
        ages = []
        totals = []

        for w in page_words:
            text = w["text"].strip().lower()

            if text == "Age":
                ages.append(w)
            elif text == "Total":
                totals.append(w)    

        # sort left -> right
        ages.sort(key=lambda w:w["x0"])
        totals.sort(key=lambda w:w["x0"])      

        # ----------------------------------------
        # Preferred method
        # ----------------------------------------

        if len(ages) >= 2 and len(totals)>= 2:
            left_total = totals[0]["x0"]
            right_age = ages[1]["x0"]

            split = (left_total + right_age) / 2

            method = "TOTAL_TO_AGE"

         # ----------------------------------------
        # Fallback
        # ----------------------------------------

        elif len(ages) >= 2:

            split = (ages[0]["x0"] + ages[1]["x0"]) / 2

            method = "AGE_TO_AGE"

        else:

            xs = sorted(w["x0"] for w in page_words)

            split = (min(xs) + max(xs)) / 2

            method = "MIDPOINT"

        splits[page] = split

        print(
            f"Page {page:<3} "
            f"Split={split:.2f} "
            f"Method={method}"
        )

    return splits
      
# -------------------------------------------------------
# Assign LEFT/RIGHT
# -------------------------------------------------------

def assign_side(words,centers):
    """
    Adds LEFT/RIGHT label to every word.
    """        
    enriched = []

    left = 0
    right = 0

    for word in words:
        page = word["page"]
        center = centers[page]

        side = "LEFT" if word["x0"] < center else "RIGHT"

        if side == "LEFT":
            left += 1
        else:
            right += 1    

        item = word.copy()
        item["side"] = side

        enriched.append(item)

    print("\n==============================")
    print("WORD COUNTS")
    print("==============================")
    print("LEFT :", left)
    print("RIGHT:", right)    

    return enriched

def remove_headers(words):
    """
    Remove page titles and running headers before row bulding
    """

    filtered = []

    skip_words = {
        "table",
        "2.3:",
        "distribution",
        "of",
        "population",
        "by",
        "age,",
        "sex*,",
        "county",
        "and",
        "sub-",
        "housing",
        "census:",
        "volume",
        "iii",
        "2019",
        "kenya",
    }

    removed = 0

    for w in words:

        text = w["text"].strip().lower()

        # running page header
        if w["top"] < 40:
            removed += 1
            continue

        # remove title words
        if text in skip_words:
            removed += 1
            continue

        filtered.append(w)

    print(f"\nRemoved {removed} header words")

    return filtered

# -------------------------------------------------------
# Group into rows
# -------------------------------------------------------

def build_side_rows(words,tolerance=2):
    """
    Groups words into rows.

    key:
        page
        side
        top
    """    
    grouped = defaultdict(list)

    for word in words:
        
        key = (
            word["page"],
            word["side"],
            round(word["top"] / tolerance) * tolerance,
        )

        grouped[key].append(word)
        
    rows = []

    for (page,side,top), row_words in sorted(grouped.items()):

        row_words.sort(key=lambda w: w["x0"])

        rows.append({
            "page": page,
            "side": side,
            "top": top,
            "row": [w["text"] for w in row_words]
        })

    left_rows = sum(r["side"] == "LEFT" for r in rows)
    right_rows = sum(r["side"] == "RIGHT" for r in rows)

    print("\n==============================")
    print("ROW COUNTS")
    print("==============================")
    print("LEFT :", left_rows)
    print("RIGHT:", right_rows)

    return rows

# -------------------------------------------------------
# Merge pages
# -------------------------------------------------------

def merge_tables(rows):
    """
    Output order:
     Page 1
      LEFT rows
      RIGHT rows

    Page 2
      LEFT rows
      RIGHT rows
    """    

    pages = defaultdict(list)

    for row in rows:
        pages[row["page"]].append(row)

    final_rows = []

    for page in sorted(pages):

        left = [
            r for r in pages[page]
            if r["side"] == "LEFT"                 
        ]    
        
        right = [
            r for r in pages[page]
            if r["side"] == "RIGHT"
        ]

        left.sort(key=lambda r:r["top"])
        right.sort(key=lambda r: r["top"])

        final_rows.extend(left)
        final_rows.extend(right)

    return final_rows    

# -------------------------------------------------------
# Save
# -------------------------------------------------------

def save_rows(rows):

    output_file = (
        VOL3_STAGING
        / f"{TABLE_2_3_VOL3['output_name']}_rows.json"
    )

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=4)

    print("\n==============================")    
    print(f"Saved {len(rows)} rows")
    print(output_file)

# -------------------------------------------------------
# Debug Preview
# -------------------------------------------------------

def preview(rows):

    print("\n==============================")
    print("FIRST 5 LEFT ROWS")
    print("==============================")

    count = 0
    for row in rows:
        if row["side"] == "LEFT":
            print(row)
            count += 1
            if count == 5:
                break

    print("\n==============================")
    print("FIRST 5 RIGHT ROWS")
    print("==============================")

    count = 0
    for row in rows:
        if row["side"] == "RIGHT":
            print(row)
            count += 1
            if count == 5:
                break

# -------------------------------------------------------
# Main
# -------------------------------------------------------            
def main():
    words = load_words()

    print(f"\nLoaded {len(words)} OCR words")

    splits = compute_page_splits(words)
    words = assign_side(words, splits)
    words = remove_headers(words)
    rows = build_side_rows(words)
    preview(rows)
    save_rows(rows)

if __name__ == "__main__":
    main()    
