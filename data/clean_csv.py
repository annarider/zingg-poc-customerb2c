import pandas as pd

# Load the CSV
df = pd.read_csv("mi_person_337_all_columns.csv")

# Select only the columns you want to keep
columns_to_keep = [
    "b_pubid",
    "b_sourceid",
    "id",
    "b_matchgrp",
    "b_xgrp",
    "normalized_first_name",
    "normalized_last_name",
    "member_id",
    "date_of_birth",
    "normalized_street",
    "normalized_city",
    "normalized_state",
    "addpostal_code",
    "addcountry",
    "cleansed_email",
    "standardized_phone",
]  # replace with your actual fields
df_clean = df[columns_to_keep]

# Save the cleaned CSV
df_clean.to_csv("mi_person_337.csv", index=False)
