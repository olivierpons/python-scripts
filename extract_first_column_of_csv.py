#!/usr/bin/env python3
"""
CSV First Column Extractor

This script extracts the content of the first column of a CSV file and outputs
the values as a comma-separated list with each value surrounded by quotes.

Example usage:
    python csv_first_column_extractor.py -i data.csv
    python csv_first_column_extractor.py --input data.csv
"""

import argparse
import csv
import sys
from pathlib import Path
from typing import List, Iterator, TextIO, Final


def parse_arguments() -> argparse.Namespace:
    """
    Parse command line arguments.

    Returns:
        argparse.Namespace: The parsed command line arguments
    """
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Extract values from the first column of a CSV file"
    )
    parser.add_argument(
        "-i", "--input", required=True, type=str, help="Path to the input CSV file"
    )
    return parser.parse_args()


def open_csv_file(file_path: str) -> TextIO:
    """
    Open a CSV file and return the file object.

    Args:
        file_path (str): Path to the CSV file

    Returns:
        TextIO: File object for the CSV file

    Raises:
        FileNotFoundError: If the file does not exist
        PermissionError: If the file cannot be read due to permission issues
    """
    try:
        return open(file_path, mode="r", encoding="utf-8", newline="")
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.", file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        print(f"Error: No permission to read '{file_path}'.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error opening file: {e}", file=sys.stderr)
        sys.exit(1)


def read_csv_first_column(file_obj: TextIO) -> List[str]:
    """
    Read the first column from a CSV file.

    Args:
        file_obj (TextIO): File object for the CSV file

    Returns:
        List[str]: First column values from the CSV
    """
    csv_reader: Iterator[List[str]] = csv.reader(file_obj)
    first_column: List[str] = []

    for row in csv_reader:
        if row and len(row) > 0:
            first_column.append(row[0])

    return first_column


def main() -> None:
    """
    Main function to process the CSV file and extract the first column values.
    """
    args: argparse.Namespace = parse_arguments()

    file_path: str = args.input
    if not Path(file_path).is_file():
        print(f"Error: '{file_path}' is not a valid file.", file=sys.stderr)
        sys.exit(1)

    with open_csv_file(file_path) as file:
        first_column_values: List[str] = read_csv_first_column(file)

    if first_column_values:
        # Format each value with quotes and join with commas
        formatted_values = [f'"{value}"' for value in first_column_values]
        print(", ".join(formatted_values))
    else:
        print("No values found in the first column.")


if __name__ == "__main__":
    main()
