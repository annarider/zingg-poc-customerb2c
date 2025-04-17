def generate_zingg_config(
    columns_to_keep, input_file_path, output_dir="/tmp/zinggOutput"
):
    field_definitions = []

    # Set matchType based on field name patterns
    for column in columns_to_keep:
        field_config = {
            "fieldName": column,
            "fields": column,  # Keep fieldName and fields identical
            "dataType": "string",
        }

        # Determine match type based on field name
        if column.startswith("b_") or column == "id":
            field_config["matchType"] = "dont_use"
        elif column in ["member_id", "date_of_birth", "person_type", "guess_gender"]:
            field_config["matchType"] = "exact"
        else:
            field_config["matchType"] = "fuzzy"

        field_definitions.append(field_config)

    # Create the complete configuration
    config = {
        "fieldDefinition": field_definitions,
        "output": [
            {
                "name": "output",
                "format": "csv",
                "props": {"location": output_dir, "delimiter": ",", "header": True},
            }
        ],
        "data": [
            {
                "name": "input_data",
                "format": "csv",
                "props": {
                    "location": input_file_path,
                    "delimiter": ",",
                    "header": True,
                },
            }
        ],
        "labelDataSampleSize": 0.5,
        "numPartitions": 4,
        "modelId": 100,
        "zinggDir": "models",
    }

    return config
