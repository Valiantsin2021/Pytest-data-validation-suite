import re
from typing import Dict, List

import pandas as pd


def parse_file(filename: str) -> pd.DataFrame:
    """
    Read JSON Lines file and convert to pandas DataFrame.

    Args:
        filename (str): Path to the JSON Lines file

    Returns:
        pd.DataFrame: DataFrame containing the parsed data
    """
    return pd.read_json(filename, lines=True)


def validate_entity_id(data: pd.DataFrame) -> List[str]:
    """
    Validate RP_ENTITY_ID format against the pattern ^[0-9A-Z]{6}$

    Args:
        data (pd.DataFrame): DataFrame containing the data to validate

    Returns:
        List[str]: List of error messages for invalid entity IDs
    """
    pattern = r"^[0-9A-Z]{6}$"

    # Create mask for invalid entity IDs
    invalid_mask = ~data["RP_ENTITY_ID"].str.match(pattern, na=False)

    # Filter rows with invalid entity IDs and format error messages
    invalid_rows = data[invalid_mask]
    failed_entity_ids = invalid_rows.apply(
        lambda row: f"RP_DOCUMENT_ID: {row['RP_DOCUMENT_ID']} with wrong format RP_ENTITY_ID: {row['RP_ENTITY_ID']}",
        axis=1,
    ).tolist()

    return failed_entity_ids


def validate_dropped_analytics(data: pd.DataFrame) -> Dict[str, List[int]]:
    """
    Identify missing record indexes for each document.

    Args:
        data (pd.DataFrame): DataFrame containing the data to validate

    Returns:
        Dict[str, List[int]]: Dictionary mapping document IDs to their missing record indexes
    """
    # Group by document ID and aggregate required data
    grouped = data.groupby("RP_DOCUMENT_ID").agg(
        {"DOCUMENT_RECORD_COUNT": "first", "DOCUMENT_RECORD_INDEX": list}
    )

    dropped_records = {}

    for doc_id, row in grouped.iterrows():
        expected_range = set(range(1, row["DOCUMENT_RECORD_COUNT"] + 1))
        actual_indexes = set(row["DOCUMENT_RECORD_INDEX"])
        missing_indexes = sorted(expected_range - actual_indexes)

        if missing_indexes:
            dropped_records[doc_id] = missing_indexes

    return dropped_records


# Optional: Add a function to perform all validations at once
def validate_data(filename: str) -> Dict[str, any]:
    """
    Perform all validations on the data file.

    Args:
        filename (str): Path to the JSON Lines file

    Returns:
        Dict containing validation results:
            - invalid_entity_ids: List of error messages for invalid entity IDs
            - dropped_records: Dictionary of documents with missing record indexes
    """
    df = parse_file(filename)
    return {
        "invalid_entity_ids": validate_entity_id(df),
        "dropped_records": validate_dropped_analytics(df),
    }
