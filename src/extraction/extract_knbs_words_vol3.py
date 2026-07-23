from config import(
    VOLUME_III_PDF,
    VOL3_STAGING,
    TABLE_2_3_VOL3,
)

from pdf_utils import extract_words_range

def main():
    output_folder = VOL3_STAGING
    output_folder.mkdir(parents=True, exist_ok=True)

    output_file = (
        output_folder
        / f"{TABLE_2_3_VOL3['output_name']}_words.json"
    )

    words = extract_words_range(
        pdf_path=VOLUME_III_PDF,
        start_page=TABLE_2_3_VOL3["start_page"],
        end_page=TABLE_2_3_VOL3["end_page"],
    )

    with open(output_file, "w", encoding="utf-8") as f:
        import json
        json.dump(words, f,indent=4)

    print(f"Extracted {len(words)} words.")
    print(f"Saved to:\n{output_file}")

if __name__ == "__main__":
    main()        