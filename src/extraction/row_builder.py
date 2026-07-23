import json
from collections import defaultdict

from config import VOL2_STAGING,TABLE_2_3_VOL2

def build_rows(words, tolerance=2):
    """
    Groups extracted words into rows based on their y-coordinates."""

    grouped = defaultdict(list)
    for word in words:

        page = word['page']

        #merge words whose y-coordinates are within the tolerance
        top =round(word["top"]/tolerance)*tolerance
        grouped[(page, top)].append(word)
    rows = []

    for (page, top), row_words in sorted(grouped.items()):

        row_words.sort(key=lambda x: x["x0"])

        rows.append(
            {
                "page": page,
                "top": top,
                "row": [w["text"] for w in row_words]
            }
        )

    return rows

def main():
    input_file = (
        VOL2_STAGING
        /f"{TABLE_2_3_VOL2['output_name']}_words.json"
    )

    output_file = (
        VOL2_STAGING
        / f"{TABLE_2_3_VOL2['output_name']}_rows.json"
    )

    with open(input_file, encoding="utf-8") as f:
        words = json.load(f)

    rows = build_rows(words)   

    with open(output_file,"w", encoding="utf-8") as f:
        json.dump(rows, f, indent=4)

    print(f"Built{len(rows)} rows.")
    print(f"Saved to:\n{output_file}")


if __name__=="__main__":
    main()