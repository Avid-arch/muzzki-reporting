import pandas as pd


def load_data(file_path):
    """
    Loads CSV data into a pandas DataFrame.
    """
    return pd.read_csv(file_path)


def find_duplicates(df, key_column):
    """
    Finds duplicate records based on a key column.
    Returns duplicate rows.
    """
    duplicates = df[df.duplicated(subset=[key_column], keep=False)]
    return duplicates


def find_missing_values(df):
    """
    Finds rows with any missing (null) values.
    Returns rows containing missing data.
    """
    missing = df[df.isnull().any(axis=1)]
    return missing


def compare_systems(df_a, df_b, key_column):
    """
    Compares two datasets based on a key column.
    Returns:
    - Records only in A
    - Records only in B
    - Records with mismatched values
    """
    df_a = df_a.set_index(key_column)
    df_b = df_b.set_index(key_column)

    # Records only in A
    only_in_a = df_a.loc[~df_a.index.isin(df_b.index)]

    # Records only in B
    only_in_b = df_b.loc[~df_b.index.isin(df_a.index)]

    # Common records
    common_keys = df_a.index.intersection(df_b.index)

    mismatches = []

    for key in common_keys:
        row_a = df_a.loc[key]
        row_b = df_b.loc[key]

        if not row_a.equals(row_b):
            mismatches.append({
                "id": key,
                "system_a": row_a.to_dict(),
                "system_b": row_b.to_dict()
            })

    return only_in_a.reset_index(), only_in_b.reset_index(), mismatches


def run_validation(file_a, file_b, key_column="id"):
    """
    Runs full validation process and returns structured results.
    """
    df_a = load_data(file_a)
    df_b = load_data(file_b)

    results = {}

    results["duplicates_a"] = find_duplicates(df_a, key_column)
    results["duplicates_b"] = find_duplicates(df_b, key_column)

    results["missing_a"] = find_missing_values(df_a)
    results["missing_b"] = find_missing_values(df_b)

    only_in_a, only_in_b, mismatches = compare_systems(df_a, df_b, key_column)

    results["only_in_a"] = only_in_a
    results["only_in_b"] = only_in_b
    results["mismatches"] = mismatches

    return results