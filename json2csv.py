import csv
import json
import os
import sys
from typing import Any

MAX_DEPTH = 5


def main():
    try:
        file_in = sys.argv[1]
        file_out = sys.argv[2]
    except IndexError as e:
        raise e("You must provide both an input file and an output file.")
    with open(file_in, "r") as f_json:
        data_json = json.load(f_json)
    data_flattened = [flatten_json(e) for e in data_json]
    headers = []
    for e in data_flattened:
        for k in e.keys():
            if k not in headers:
                headers.append(k)
    overwrite = ""
    out_file_exists = os.path.isfile(file_out)
    if out_file_exists:
        overwrite = input(
            f"Output file {file_out} already exists. "
            "Would you like to overwrite it? (y/n): "
        )
    if overwrite.lower() == "y" or not out_file_exists:
        with open(file_out, "w", newline="") as f_csv:
            wrtr = csv.DictWriter(f_csv, fieldnames=headers)
            wrtr.writeheader()
            wrtr.writerows(data_flattened)


def flatten_json(json_data: dict[str, Any]) -> dict[str, str]:
    """Flatten the dictionary to remove any nesting and create the CSV headers.

    Args:
        json_data (dict[str, Any]): initial dictionary

    Returns:
        dict[str, str]: flattened dictionary
    """
    out = {}
    for key, value in json_data.items():
        if isinstance(value, dict):
            flattened = flatten_json(value)
            for sub_key, sub_value in flattened.items():
                out[key + "." + sub_key] = sub_value
        elif isinstance(value, list):
            for i, item in enumerate(value):
                if isinstance(item, dict):
                    flattened = flatten_json(item)
                    for sub_key, sub_value in flattened.items():
                        out[key + "." + str(i) + "." + sub_key] = sub_value
                else:
                    out[key + "." + str(i)] = item
        else:
            out[key] = value
    return out


if __name__ == "__main__":
    main()
