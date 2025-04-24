import pandas as pd


def create_zingg_training_data(input_csv, output_csv):
    # Read the CSV file
    df = pd.read_csv(input_csv)

    # Columns to keep
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
    ]

    # Filter dataframe to keep only specified columns
    df = df[columns_to_keep]

    # Create empty lists to store processed records
    processed_records = []

    # Group by golden ID
    by_golden = {}
    for _, row in df.iterrows():
        golden_id = row["id"]

        if golden_id not in by_golden:
            by_golden[golden_id] = []

        by_golden[golden_id].append(row.to_dict())

    # Create match clusters (same golden ID)
    cluster_id = 1
    for golden_id, records in by_golden.items():
        if len(records) > 1:  # Only create clusters with multiple records
            for record in records:
                record["z_cluster"] = f"match_{cluster_id}"
                record["z_isMatch"] = 1
                processed_records.append(record)
            cluster_id += 1

    # Group by exclusion group
    by_xgrp = {}
    for _, row in df.iterrows():
        xgrp = row.get("b_xgrp")
        if pd.notna(xgrp):  # Check if xgrp is not NaN
            if xgrp not in by_xgrp:
                by_xgrp[xgrp] = []
            by_xgrp[xgrp].append(row.to_dict())

    # Create non-match clusters from exclusion groups with different golden IDs
    for xgrp, xgrp_records in by_xgrp.items():
        golden_ids = set(r["id"] for r in xgrp_records)
        if len(golden_ids) > 1:  # Different golden IDs in same exclusion group
            for record in xgrp_records:
                record["z_cluster"] = f"nonmatch_{cluster_id}"
                record["z_isMatch"] = 0
                processed_records.append(record)
            cluster_id += 1

    # Convert to DataFrame and save to CSV
    result_df = pd.DataFrame(processed_records)

    # Ensure final columns are correct (original columns plus Zingg columns)
    final_columns = columns_to_keep + ["z_cluster", "z_isMatch"]
    result_df = result_df[final_columns]

    result_df.to_csv(output_csv, index=False)

    # Summary statistics
    match_count = sum(1 for r in processed_records if r["z_isMatch"] == 1)
    nonmatch_count = sum(1 for r in processed_records if r["z_isMatch"] == 0)
    match_clusters = len(
        set(r["z_cluster"] for r in processed_records if r["z_isMatch"] == 1)
    )
    nonmatch_clusters = len(
        set(r["z_cluster"] for r in processed_records if r["z_isMatch"] == 0)
    )

    print(f"Created {match_count} match records in {match_clusters} clusters")
    print(f"Created {nonmatch_count} non-match records in {nonmatch_clusters} clusters")
    print(
        f"Total: {len(processed_records)} records in {match_clusters + nonmatch_clusters} clusters"
    )


# Usage
if __name__ == "__main__":
    create_zingg_training_data(
        "2025-04-24_mi_um_person.csv", "2025-04-24_zingg_training_data.csv"
    )
