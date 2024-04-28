import argparse
import csv
import json
import os
from typing import Any

MAX_DEPTH = 5


def main(args: argparse.Namespace):
    json_file = args[0]
    csv_file = args[1]
    sep = args[2]
    with open(json_file, "r") as f_json:
        data_json = json.load(f_json)
    if isinstance(data_json, list):
        data_flattened = [flatten_json(e, sep) for e in data_json]
    elif isinstance(data_json, dict):
        data_flattened = flatten_json(data_json, sep)
    headers = []
    for e in data_flattened:
        for k in e.keys():
            if k not in headers:
                headers.append(k)
    overwrite = ""
    out_file_exists = os.path.isfile(csv_file)
    if out_file_exists:
        overwrite = input(
            f"Output file {csv_file} already exists. "
            "Would you like to overwrite it? (y/n): "
        )
    if overwrite.lower() == "y" or not out_file_exists:
        with open(csv_file, "w", newline="") as f_csv:
            wrtr = csv.DictWriter(f_csv, fieldnames=headers)
            wrtr.writeheader()
            wrtr.writerows(data_flattened)


def flatten_json(json_data: dict[str, Any], sep: str) -> dict[str, str]:
    """Flatten the dictionary to remove any nesting and create the CSV headers.

    Args:
        json_data (dict[str, Any]): initial dictionary

    Returns:
        dict[str, str]: flattened dictionary
    """
    out = {}
    for key, value in json_data.items():
        if isinstance(value, dict):
            flattened = flatten_json(value, sep)
            for sub_key, sub_value in flattened.items():
                out[f"{key}{sep}{sub_key}"] = sub_value
        elif isinstance(value, list):
            for i, item in enumerate(value):
                if isinstance(item, dict):
                    flattened = flatten_json(item, sep)
                    for sub_key, sub_value in flattened.items():
                        out[f"{key}{sep}{str(i)}{sep}{sub_key}"] = sub_value
                else:
                    out[f"{key}{sep}{str(i)}"] = item
        else:
            out[key] = value
    return out


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert a JSON file to a CSV file.")
    parser.add_argument("json_file", type=str, help="path to the JSON input file")
    parser.add_argument("csv_file", type=str, help="path to the CSV output file")
    parser.add_argument(
        "--sep",
        type=str,
        default=".",
        help="custom separator for flattened keys. defaults to '.'",
    )
    args = parser.parse_args()
    main(args)
