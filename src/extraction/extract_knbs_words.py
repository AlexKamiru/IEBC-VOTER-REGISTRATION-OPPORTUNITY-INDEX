from pathlib import Path
import json

from config import (
    VOLUME_II_PDF,
    VOL2_STAGING,
    TABLE_2_3_VOL2,
)

from pdf_utils import extract_words_range

def main():

    output_folder = VOL2_STAGING
    output_folder.mkdir(parents=True, exist_ok=True)

    output_file = (
        output_folder 
        / f"{TABLE_2_3_VOL2['output_name']}_words.json")

    words = extract_words_range(
        pdf_path = VOLUME_II_PDF,
        start_page = TABLE_2_3_VOL2["start_page"],
        end_page = TABLE_2_3_VOL2["end_page"],
    )

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(words, f, ensure_ascii=False, indent=4)

    print(f"Extracted {len(words)} words .")
    print(f"Saved to:\n{output_file}")


if __name__ == "__main__":
    main()