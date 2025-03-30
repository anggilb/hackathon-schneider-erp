import sqlite3

DB_FILE = "sql_queries/erp.db"


# Connect to SQLite database. Do not change this. Call this function within each of the requested functions.
def get_db_connection(db_file):
    return sqlite3.connect(db_file)


# Query 1: Top selling products
def get_top_selling_products(db_file):
    """
    Create a new table in the database schema named "TopSellingProducts" with the top 3 selling products in each category.
    Return the table with the following schema:

    |-----------------|-------------|--------------------|------------------|
    | category (text) | name (text) | total_sales (real) | sales_rank (int) |
    |-----------------|-------------|--------------------|------------------|

    """
    pass
    conn = get_db_connection(db_file)
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS TopSellingProducts')

    cursor.execute('''
    CREATE TABLE TopSellingProducts (
        category TEXT,
        name TEXT,
        total_sales REAL,
        sales_rank INTEGER
    );
    ''')

    cursor.execute('''
    WITH ProductSales AS (
        SELECT 
            p.category, 
            p.name, 
            SUM(od.quantity) AS total_sales
        FROM Products p
        JOIN OrderDetails od ON p.product_id = od.product_id
        GROUP BY p.category, p.name
    ),
    RankedProducts AS (
        SELECT 
            category, 
            name, 
            ROUND(total_sales, 2) AS total_sales,
            RANK() OVER (PARTITION BY category ORDER BY total_sales DESC) AS sales_rank
        FROM ProductSales
    )
    INSERT INTO TopSellingProducts
    SELECT category, name, total_sales, sales_rank
    FROM RankedProducts
    WHERE sales_rank <= 3
    ORDER BY category, sales_rank, total_sales DESC;
    ''')

    conn.commit()
    conn.close()


# Query 2: Percentage of Orders That Were Delivered Late
def get_late_deliveries(db_file):
    """
    Return the percentage of late deliveries. Consider a policy of maximuim 5 day delivery.

    """
    pass
    conn = get_db_connection(db_file)
    cursor = conn.cursor()

    query = '''
    WITH DeliveredOrders AS (
        SELECT 
            order_id,
            julianday(delivery_date) - julianday(order_date) AS delivery_days
        FROM Orders
        WHERE status = 'Delivered'
        AND delivery_date IS NOT NULL
        AND order_date IS NOT NULL
    )
    SELECT 
        ROUND(
            COUNT(CASE WHEN delivery_days > 5 THEN 1 END) * 100.0 / NULLIF(COUNT(*), 0), 
            2
        ) AS late_delivery_percentage
    FROM DeliveredOrders;
    '''
    cursor.execute(query)
    result = cursor.fetchone()[0]
    conn.close()
    return result

# Query 3: Customer Sales Performance
def get_customer_sales_performance(db_file):
    conn = get_db_connection(db_file)
    cursor = conn.cursor()

    cursor.execute('DROP TABLE IF EXISTS CustomerSalesPerformance')

    cursor.execute('''
    CREATE TABLE CustomerSalesPerformance (
        customer_id INTEGER,
        total_orders INTEGER,
        total_revenue REAL,
        avg_order_value REAL,
        revenue_rank INTEGER,
        customer_category TEXT
    );
    ''')

    cursor.execute('''
    WITH CustomerAggregates AS (
        SELECT 
            c.customer_id,
            COUNT(o.order_id) AS total_orders,
            SUM(od.total_price) AS total_revenue_raw,
            AVG(od.total_price) AS avg_order_value_raw
        FROM Customers c
        JOIN Orders o ON c.customer_id = o.customer_id
        JOIN OrderDetails od ON o.order_id = od.order_id
        GROUP BY c.customer_id
    ),
    AverageRevenue AS (
        SELECT AVG(total_revenue_raw) AS avg_revenue
        FROM CustomerAggregates
    ),
    RankedCustomers AS (
        SELECT 
            ca.customer_id,
            ca.total_orders,
            ROUND(ca.total_revenue_raw, 2) AS total_revenue,
            ROUND(ca.avg_order_value_raw, 2) AS avg_order_value,
            RANK() OVER (ORDER BY ca.total_revenue_raw DESC) AS revenue_rank,
            CASE 
                WHEN ca.total_revenue_raw > ar.avg_revenue THEN 'High-Value Customer'
                ELSE 'Regular Customer'
            END AS customer_category
        FROM CustomerAggregates ca
        CROSS JOIN AverageRevenue ar
    )
    INSERT INTO CustomerSalesPerformance
    SELECT * FROM RankedCustomers;
    ''')

    conn.commit()
    conn.close()

# Query 4: Inventory & Sales Forecast Table
def get_sales_forecast(db_file):
    """
    Create a new table in the database schema named "SalesForecast" based on the last 3 months of purchases
    Return the table with the following schema:

    |------------------|---------------------|----------------------|---------------------------|----------------------------------------|------------------|
    | product_id (int) | product_name (text) | stock_quantity (int) | sales_last_3_months (int) | estimated_months_before_stockout (int) | stock_rank (int) |
    |------------------|---------------------|----------------------|---------------------------|----------------------------------------|------------------|

    """
    pass

    conn = get_db_connection(db_file)
    cursor = conn.cursor()

    cursor.execute('DROP TABLE IF EXISTS SalesForecast')
    cursor.execute('''
    CREATE TABLE SalesForecast (
        product_id INTEGER,
        product_name TEXT,
        stock_quantity INTEGER,
        sales_last_3_months INTEGER,
        estimated_months_before_stockout INTEGER,
        stock_rank INTEGER
    );
    ''')

    cursor.execute('DELETE FROM SalesForecast')

    cursor.execute('''
    WITH InventoryAgg AS (
        SELECT product_id, SUM(stock_quantity) AS stock_quantity
        FROM Inventory
        GROUP BY product_id
    ),
    Last3MonthsSales AS (
        SELECT od.product_id, SUM(od.quantity) AS sales_last_3_months
        FROM OrderDetails od
        JOIN Orders o ON od.order_id = o.order_id
        WHERE o.order_date >= DATE('now', '-3 months')
        GROUP BY od.product_id
    )
    INSERT INTO SalesForecast
    SELECT 
        p.product_id,
        p.name AS product_name,
        CAST(COALESCE(i.stock_quantity, 0) AS INTEGER) AS stock_quantity,
        CAST(COALESCE(s.sales_last_3_months, 0) AS INTEGER) AS sales_last_3_months,
        CASE 
            WHEN s.sales_last_3_months IS NULL OR s.sales_last_3_months = 0 THEN -1
            ELSE CAST(ROUND(COALESCE(i.stock_quantity, 0) * 3.0 / s.sales_last_3_months, 0) AS INTEGER)
        END AS estimated_months_before_stockout,
        DENSE_RANK() OVER (ORDER BY COALESCE(i.stock_quantity, 0) DESC) AS stock_rank
    FROM Products p
    LEFT JOIN InventoryAgg i ON p.product_id = i.product_id
    LEFT JOIN Last3MonthsSales s ON p.product_id = s.product_id
    ORDER BY p.product_id;
    ''')
    conn.commit()
    conn.close()

# Query 5: Order Profitability & Discount Analysis
def get_discount_analysis(db_file):
    conn = get_db_connection(db_file)
    cursor = conn.cursor()

    cursor.execute('DROP TABLE IF EXISTS DiscountAnalysis')

    cursor.execute('''
    CREATE TABLE DiscountAnalysis (
        order_id INTEGER,
        total_revenue REAL,
        total_cost REAL,
        profit REAL,
        profit_margin_percentage REAL,
        discount_percentage REAL,
        profitability_rank INTEGER
    );
    ''')

    cursor.execute('''
    WITH order_totals AS (
        SELECT 
            o.order_id,
            ROUND(SUM(od.total_price), 2) AS total_revenue,
            ROUND(SUM(p.price * 0.7 * od.quantity), 2) AS total_cost,
            ROUND(SUM(od.total_price) - SUM(p.price * 0.7 * od.quantity), 2) AS profit,
            ROUND((SUM(od.total_price) - SUM(p.price * 0.7 * od.quantity)) * 100.0 / NULLIF(SUM(od.total_price), 0), 2) AS profit_margin_percentage
        FROM Orders o
        JOIN OrderDetails od ON o.order_id = od.order_id
        JOIN Products p ON od.product_id = p.product_id
        GROUP BY o.order_id
    ),
    line_discounts AS (
        SELECT 
            od.order_id,
            ROUND((p.price * od.quantity - od.total_price) * 100.0 / NULLIF(p.price * od.quantity, 1), 2) AS discount_percentage
        FROM OrderDetails od
        JOIN Products p ON od.product_id = p.product_id
        WHERE p.price * od.quantity != 0
    )
    INSERT INTO DiscountAnalysis
    SELECT 
        ot.order_id,
        ot.total_revenue,
        ot.total_cost,
        ot.profit,
        ot.profit_margin_percentage,
        ld.discount_percentage,
        RANK() OVER (ORDER BY ot.profit DESC) AS profitability_rank
    FROM order_totals ot
    JOIN line_discounts ld ON ot.order_id = ld.order_id
    ORDER BY ot.profit DESC;
    ''')

    conn.commit()
    conn.close()


if __name__ == "__main__":
    get_top_selling_products(DB_FILE)
    print(get_late_deliveries(DB_FILE))
    get_customer_sales_performance(DB_FILE)
    get_sales_forecast(DB_FILE)
    get_discount_analysis(DB_FILE)
