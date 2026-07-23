from pathlib import Path

#Project Root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

#Raw Data
Raw_Data = PROJECT_ROOT/"data" /"raw"

# KNBS
KNBS_RAW = Raw_Data/ "KNBS"

VOLUME_II_PDF =(
    KNBS_RAW
    /"Volume_II"
    /"2019-Kenya-population-and-Housing-Census-Volume-2-Distribution-of-Population-by-Administrative-Units.pdf"
)

VOLUME_III_PDF = (
    KNBS_RAW
    /"Volume_III"
    /"2019-Kenya-Population-and-Housing-Census-Volume-3-Distribution-of-Population-by-Age-and-Sex.pdf"
)

VOLUME_IV_PDF = (
    KNBS_RAW
    /"Volume_IV"
    /"2019-Kenya-Population-and-Housing-Census-Volume-4-Distribution-of-Population-by-Socio-Economic-Characteristics.pdf"
)

# Table configuration
TABLE_2_3_VOL2 = {
    "start_page": 24,
    "end_page": 30,
    "output_name": "knbs_vol2_table_2_3",
}

TABLE_2_3_VOL3 = {
    "start_page": 29,
    "end_page": 420,
    "output_name": "knbs_vol3_table_2_3",

    #midpoint between the two tables(left and right)
    "page_split": 340
}

#Staging
STAGING = PROJECT_ROOT/"data"/"staging"

KNBS_STAGING = STAGING/"knbs"

VOL2_STAGING = KNBS_STAGING / "volume_ii"
VOL3_STAGING = KNBS_STAGING / "volume_iii"

#processed
PROCESSED = PROJECT_ROOT/ "data"/"processed"
KNBS_PROCESSED = PROCESSED /"knbs"

VOL2_PROCESSED = KNBS_PROCESSED / "volume_ii"
VOL3_PROCESSED = KNBS_PROCESSED / "volume_iii"
