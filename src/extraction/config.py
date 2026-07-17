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

# Table configuration
TABLE_2_3 = {
    "start_page": 24,
    "end_page": 30,
    "output_name": "knbs_vol2_table_2_3",
}

#Staging
STAGING = PROJECT_ROOT/"data"/"staging"

KNBS_STAGING = STAGING/"knbs"

#processed
PROCESSED = PROJECT_ROOT/ "data"/"processed"
KNBS_PROCESSED = PROCESSED /"knbs"

