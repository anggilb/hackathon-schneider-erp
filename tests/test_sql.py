import sqlite3
from sql_queries.solution import (
    get_customer_sales_performance,
    get_discount_analysis,
    get_sales_forecast,
    get_late_deliveries,
    get_top_selling_products,
)


DB_FILE = "sql_queries/erp.db"


def get_db_connection():
    return sqlite3.connect(DB_FILE)


def compare_rows(actual_rows, expected_rows):
    assert len(actual_rows) == len(
        expected_rows
    ), f"Expected {len(expected_rows)} rows but got {len(actual_rows)}"

    # Optional sort if order doesn't matter
    actual_rows_sorted = sorted(actual_rows)
    expected_rows_sorted = sorted(expected_rows)

    for idx, (actual, expected) in enumerate(
        zip(actual_rows_sorted, expected_rows_sorted)
    ):
        assert (
            actual == expected
        ), f"Row {idx} mismatch: Expected {expected}, got {actual}"


def fetch_data_from_db(query):
    """
    Executes a SQL query and returns the result rows.
    """
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    cur.execute(query)
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows


# --------------------------- #
#  Test: Top Selling Products
# --------------------------- #


def test_1_top_selling_products_table_exists():
    get_top_selling_products(DB_FILE)
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='TopSellingProducts';"
    )
    result = cur.fetchone()
    cur.close()
    conn.close()
    assert result is not None


def test_2_top_selling_products_schema():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(TopSellingProducts);")
    columns = [col[1] for col in cur.fetchall()]
    expected_columns = ["category", "name", "total_sales", "sales_rank"]
    cur.close()
    conn.close()
    assert all(col in columns for col in expected_columns)


def test_3_top_selling_products_data():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM TopSellingProducts WHERE sales_rank <= 3;")
    count = cur.fetchone()[0]
    assert count > 0

    cur.close()
    conn.close()


def test_4_top_selling_products_data():
    actual_rows = fetch_data_from_db("SELECT * FROM TopSellingProducts;")
    expected_rows = [
        ("Electrical", "Circuit Breaker", 25.0, 1),
        ("Electrical", "Transformer", 7.0, 2),
        ("Electrical", "Industrial Switchgear", 3.0, 3),
        ("IoT", "Smart Meter", 8.0, 1),
        ("Renewable Energy", "Battery Storage", 4.0, 1),
        ("Renewable Energy", "Solar Inverter", 3.0, 2),
    ]

    compare_rows(actual_rows, expected_rows)


# --------------------- #
# Test: Late Deliveries
# -------------------- #


def test_1_late_deliveries_returns_value():
    percentage = get_late_deliveries(DB_FILE)
    assert isinstance(percentage, float)


def test_2_late_deliveries_percentage_range():
    percentage = get_late_deliveries(DB_FILE)
    assert 0.0 <= percentage <= 100.0


def test_3_late_deliveries_percentage_range():
    percentage = get_late_deliveries(DB_FILE)
    assert percentage == 40.0


# ------------------ #
# Test: Customer Sales Performance
# ------------------ #


def test_1_customer_sales_table_exists():
    get_customer_sales_performance(DB_FILE)

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='CustomerSalesPerformance';"
    )
    result = cur.fetchone()
    cur.close()
    conn.close()
    assert result is not None


def test_2_customer_sales_schema():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(CustomerSalesPerformance);")
    columns = [col[1] for col in cur.fetchall()]
    expected_columns = [
        "customer_id",
        "total_orders",
        "total_revenue",
        "avg_order_value",
        "revenue_rank",
        "customer_category",
    ]
    cur.close()
    conn.close()
    assert all(col in columns for col in expected_columns)


def test_3_customer_sales_data():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM CustomerSalesPerformance;")
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    assert count > 0


def test_4_customer_sales_data():
    actual_rows = fetch_data_from_db("SELECT * FROM CustomerSalesPerformance;")
    expected_rows = [
        (1, 3, 4250.0, 1416.67, 1, "High-Value Customer"),
        (3, 2, 4200.0, 2100.0, 2, "High-Value Customer"),
        (2, 2, 3550.0, 1775.0, 3, "High-Value Customer"),
        (5, 2, 2600.0, 1300.0, 4, "Regular Customer"),
        (4, 1, 1800.0, 1800.0, 5, "Regular Customer"),
    ]

    compare_rows(actual_rows, expected_rows)


# ------------------ #
# Test: Sales Forecast
# ------------------ #


def test_1_sales_forecast_table_exists():
    get_sales_forecast(DB_FILE)
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='SalesForecast';"
    )
    result = cur.fetchone()
    cur.close()
    conn.close()
    assert result is not None


def test_2_sales_forecast_schema():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(SalesForecast);")
    columns = [col[1] for col in cur.fetchall()]
    expected_columns = [
        "product_id",
        "product_name",
        "stock_quantity",
        "sales_last_3_months",
        "estimated_months_before_stockout",
        "stock_rank",
    ]
    cur.close()
    conn.close()
    assert all(col in columns for col in expected_columns)


def test_3_sales_forecast_data():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM SalesForecast;")
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    assert count > 0


def test_4_sales_forecast_data():
    actual_rows = fetch_data_from_db("SELECT * FROM SalesForecast;")
    expected_rows = [
        (3, "Solar Inverter", 950, 3, 950, 1),
        (2, "Transformer", 630, 7, 270, 2),
        (1, "Circuit Breaker", 620, 25, 74, 3),
        (4, "Battery Storage", 510, 4, 383, 4),
        (5, "Smart Meter", 460, 8, 173, 5),
        (6, "Industrial Switchgear", 230, 3, 230, 6)
    ]

    compare_rows(actual_rows, expected_rows)


# ---------------------- #
# Test: Discount Analysis
# ---------------------- #


def test_1_discount_analysis_table_exists():
    get_discount_analysis(DB_FILE)

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='DiscountAnalysis';"
    )
    result = cur.fetchone()
    cur.close()
    conn.close()
    assert result is not None


def test_2_discount_analysis_schema():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(DiscountAnalysis);")
    columns = [col[1] for col in cur.fetchall()]
    expected_columns = [
        "order_id",
        "total_revenue",
        "total_cost",
        "profit",
        "profit_margin_percentage",
        "discount_percentage",
        "profitability_rank",
    ]
    cur.close()
    conn.close()
    assert all(col in columns for col in expected_columns)


def test_3_discount_analysis_data():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM DiscountAnalysis;")
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    assert count > 0


def test_4_discount_analysis_data():
    actual_rows = fetch_data_from_db("SELECT * FROM DiscountAnalysis;")
    expected_rows = [
        (103, 3200.0, 2240.0, 960.0, 30.0, 0.0, 1),
        (101, 3250.0, 2450.0, 800.0, 24.62, 0.0, 2),
        (101, 3250.0, 2450.0, 800.0, 24.62, 25.0, 2),
        (102, 2350.0, 1680.0, 670.0, 28.51, 2.08, 4),
        (105, 2100.0, 1470.0, 630.0, 30.0, 0.0, 5),
        (104, 1800.0, 1260.0, 540.0, 30.0, 0.0, 6),
        (108, 1200.0, 840.0, 360.0, 30.0, 0.0, 7),
        (107, 1000.0, 700.0, 300.0, 30.0, 0.0, 8),
        (109, 500.0, 420.0, 80.0, 16.0, 16.67, 9),
        (106, 1000.0, 1050.0, -50.0, -5.0, 33.33, 10),
    ]

    compare_rows(actual_rows, expected_rows)
