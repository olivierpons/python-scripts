import pandas as pd
import argparse
import os
from typing import NoReturn
from tabulate import tabulate


def main() -> NoReturn:
    """
    Process a CSV file to remove duplicates and save them separately.

    This script reads a CSV file, identifies duplicate entries, removes them
    from the main file and saves them in a separate file. It works with any CSV
    file regardless of its content or the number of columns.

    The script uses argparse to handle command-line arguments and tabulate
    to present a summary of the results.
    """
    # Setup argument parser
    parser = argparse.ArgumentParser(
        description="Process a CSV file to remove duplicates"
    )
    parser.add_argument("input_file", type=str, help="Path to the input CSV file")
    parser.add_argument(
        "output_file", type=str, help="Path to the output CSV file (without duplicates)"
    )
    parser.add_argument(
        "duplicates_file", type=str, help="Path to the CSV file containing duplicates"
    )
    parser.add_argument(
        "--encoding",
        type=str,
        default="utf-8",
        help="CSV file encoding (default: utf-8)",
    )
    parser.add_argument(
        "--delimiter", type=str, default=",", help="CSV file delimiter (default: ,)"
    )
    parser.add_argument(
        "--table-format",
        type=str,
        default="fancy_grid",
        help="Format for summary table (default: fancy_grid)",
    )

    # Parse arguments
    args = parser.parse_args()

    # Check if input file exists
    if not os.path.exists(args.input_file):
        print(f"Error: File {args.input_file} does not exist.")
        return

    try:
        # Read the CSV file
        print(f"Reading file {args.input_file}...")
        df: pd.DataFrame = pd.read_csv(
            args.input_file, encoding=args.encoding, delimiter=args.delimiter
        )

        # Get column information
        columns_count: int = len(df.columns)
        columns_names: list[str] = df.columns.tolist()

        # Identify duplicates
        print("Searching for duplicates...")
        duplicates: pd.DataFrame = df[df.duplicated(keep="first")]

        # Remove duplicates from the main file
        print("Removing duplicates...")
        df_clean: pd.DataFrame = df.drop_duplicates(keep="first")

        # Save the file without duplicates
        print(f"Saving file without duplicates to {args.output_file}...")
        df_clean.to_csv(
            args.output_file, index=False, encoding=args.encoding, sep=args.delimiter
        )

        # Save duplicates to a separate file
        print(f"Saving duplicates to {args.duplicates_file}...")
        duplicates.to_csv(
            args.duplicates_file,
            index=False,
            encoding=args.encoding,
            sep=args.delimiter,
        )

        # Display statistics using tabulate
        print("\nPROCESSING SUMMARY:")

        # Basic summary
        summary_data: list[list[str | int]] = [
            ["Original file", args.input_file, len(df), "rows"],
            [
                "Output file (without duplicates)",
                args.output_file,
                len(df_clean),
                "rows",
            ],
            ["Duplicates file", args.duplicates_file, len(duplicates), "rows"],
            [
                "Duplicates removed",
                "",
                len(duplicates),
                f"({(len(duplicates) / len(df) * 100):.2f}%)",
            ],
        ]

        print(
            tabulate(
                summary_data,
                headers=["File Type", "Path", "Count", "Unit"],
                tablefmt=args.table_format,
            )
        )

        # Column information
        print("\nCOLUMN INFORMATION:")
        column_data: list[list[str | int]] = [
            ["Total columns", columns_count],
        ]
        for i, col in enumerate(columns_names, 1):
            column_data.append([f"Column {i}", col])

        print(
            tabulate(column_data, headers=["Item", "Value"], tablefmt=args.table_format)
        )

        # Sample of duplicate rows if any exist
        if len(duplicates) > 0:
            print("\nSAMPLE OF DUPLICATE ROWS (max 5):")
            sample_df: pd.DataFrame = duplicates.head(5)
            print(
                tabulate(sample_df, headers=columns_names, tablefmt=args.table_format)
            )

            if len(duplicates) > 5:
                print(f"... and {len(duplicates) - 5} more duplicate rows.")

    except Exception as e:
        print(f"Error processing the file: {e}")


def process_csv_file(
    input_file: str,
    output_file: str,
    duplicates_file: str,
    encoding: str = "utf-8",
    delimiter: str = ",",
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Process a CSV file to remove duplicates and save them separately.

    Args:
        input_file: Path to the input CSV file.
        output_file: Path to the output CSV file (without duplicates).
        duplicates_file: Path to the CSV file containing duplicates.
        encoding: CSV file encoding. Defaults to 'utf-8'.
        delimiter: CSV file delimiter. Defaults to ','.

    Returns:
        A tuple containing two dataframes:
            - The dataframe without duplicates
            - The dataframe containing only duplicates

    Raises:
        FileNotFoundError: If the input file does not exist.
        Exception: For any other error during file processing.
    """
    # Check if input file exists
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"File {input_file} does not exist.")

    # Read the CSV file
    df: pd.DataFrame = pd.read_csv(input_file, encoding=encoding, delimiter=delimiter)

    # Identify duplicates
    duplicates: pd.DataFrame = df[df.duplicated(keep="first")]

    # Remove duplicates from the main file
    df_clean: pd.DataFrame = df.drop_duplicates(keep="first")

    # Save the file without duplicates
    df_clean.to_csv(output_file, index=False, encoding=encoding, sep=delimiter)

    # Save duplicates to a separate file
    duplicates.to_csv(duplicates_file, index=False, encoding=encoding, sep=delimiter)

    return df_clean, duplicates


if __name__ == "__main__":
    main()
