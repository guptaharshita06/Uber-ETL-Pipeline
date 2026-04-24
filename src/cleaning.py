import pandas as pd

def clean_data(df, remove_duplicates=True, handle_missing=True, fill_method="mean"):
    df.columns = df.columns.str.strip()

    # convert datetime
    for col in df.columns:
        if 'date' in col.lower() or 'time' in col.lower():
            df[col] = pd.to_datetime(df[col], errors='coerce')

    # convert numeric strings to numbers
    for col in df.columns:
        try:
            df[col] = pd.to_numeric(df[col])
        except:
            pass

    # remove duplicates
    if remove_duplicates:
        df = df.drop_duplicates()

    # handle missing values
    if handle_missing:
        if fill_method == "mean":
            for col in df.select_dtypes(include='number'):
                df[col] = df[col].fillna(df[col].mean())

        elif fill_method == "median":
            for col in df.select_dtypes(include='number'):
                df[col] = df[col].fillna(df[col].median())

        elif fill_method == "zero":
            df = df.fillna(0)

        elif fill_method == "drop":
            df = df.dropna()

    return df