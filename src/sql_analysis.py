import sqlite3

def run_sql_queries(df):
    conn = sqlite3.connect("data.db")

    # load dataframe into SQL table
    df.to_sql("data_table", conn, if_exists="replace", index=False)

    # total rows
    total = conn.execute("SELECT COUNT(*) FROM data_table").fetchone()[0]

    # get numeric columns
    numeric_cols = df.select_dtypes(include='number').columns

    avg_values = {}

    for col in numeric_cols:
        try:
            avg = conn.execute(f"SELECT AVG({col}) FROM data_table").fetchone()[0]
            avg_values[col] = avg
        except:
            pass

    conn.close()

    return total, avg_values