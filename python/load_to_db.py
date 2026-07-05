import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

EXCEL_FILE = BASE_DIR / "data" / "Analytics_Quiz_Data_Analyst.xlsx"
DB_DIR = BASE_DIR / "database"
DB_FILE = DB_DIR / "quiz.db"

DB_DIR.mkdir(parents=True, exist_ok=True)


def load_sales(conn):
    """
    Лист SQL: заголовки на строке 5 (индекс 4), данные с строки 6.
    """

    df = pd.read_excel(EXCEL_FILE, sheet_name="SQL", usecols="A:C", header=4)
    df.columns = ["OrderDate", "SKU", "UnitsSold"]
    df = df.dropna(subset=["SKU", "UnitsSold"]).copy()
    df["OrderDate"] = pd.to_datetime(df["OrderDate"]).dt.strftime("%Y-%m-%d")
    df["UnitsSold"] = df["UnitsSold"].astype(int)
    df.to_sql("sales", conn, if_exists="replace", index=False)
    print(f"[sales]   загружено строк: {len(df)}")


def load_defects(conn):
    """
    Лист Visualization: заголовки на строке 3 (индекс 2), данные с строки 4.
    """

    df = pd.read_excel(EXCEL_FILE, sheet_name="Visualization", header=2)
    df.columns = ["Date", "Orders", "Defects", "Revenue", "Profit"]
    df = df.dropna(subset=["Orders"]).copy()
    df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m-%d")
    for col in ["Orders", "Defects", "Revenue", "Profit"]:
        df[col] = df[col].astype(int)
    df.to_sql("defects", conn, if_exists="replace", index=False)
    print(f"[defects] загружено строк: {len(df)}")


def main():
    conn = sqlite3.connect(DB_FILE)
    load_sales(conn)
    load_defects(conn)
    n1 = conn.execute("SELECT COUNT(*) FROM sales").fetchone()[0]
    n2 = conn.execute("SELECT COUNT(*) FROM defects").fetchone()[0]
    print(f"\nГотово! База: {DB_FILE}")
    print(f"  sales   = {n1} строк (ожидается 740)")
    print(f"  defects = {n2} строк (ожидается 365)")
    conn.close()


if __name__ == "__main__":
    main()
