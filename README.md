# 🏢 Python ERP Challenge 🐍

Category   ➡️   Software

Subcategory   ➡️   Python 

Difficulty   ➡️   Medium

---

## 🌐 Background
ERP systems are the backbone of business operations, managing everything from inventory to financials. In this challenge, you’ll take on the task of modernizing an ERP system using Python, tackling real-world problems in data processing, API development, and business analytics.

You’ll build a data pipeline that transforms and validates information from multiple sources, ensuring accuracy and efficiency. A Flask-based API will connect to a legacy ERP system, retrieving product stock details and locating the nearest technicians using geolocation. SQL queries will help analyze business performance, forecast inventory needs, and evaluate profitability. Along the way, algorithmic challenges will test your ability to optimize data processing and solve logic-based problems.

## 📂 Repository Structure
```

├── algorithms/
│   └── functions.py
│
├── api_rest/
│   └── main.py
│
├── data_transformation/
│   ├── inputs/
│   │   ├── records.json
│   ├── outputs/
│   │   ├── details.csv
│   │   └── transactions.csv
│   ├── config.yaml
│   └── main.py
│
├── questions/
│   └── answers.json
│
├── sql_queries/
│   ├── setup_database.py
│   ├── setup.sql
│   └── solution.py
│
└── README.md

      
```
## 🎯 Tasks


### 1. Data Ingestion Pipeline Task – Transformation, Mapping & Validation
Develop a data ingestion pipeline that processes data ensuring transformation, mapping, and validation before exporting it to a structured CSV format.    
- **Input Format:** JSON
- **Output Format:** CSV 
- **Configuration:** A `config.yml` defining target field mappings.
- **Pipeline Features:**
    1. Data Transformation:
        - Convert various input formats into a standardized CSV structure.
    2. Data Mapping and Validation:
        - Map source fields to the target CSV schema.
        - Use regex and Pydantic for field validation and data cleaning.
    3. Type Conversion & Error Handling:
        - Manage missing fields and invalid data types.
        - Provide default values where applicable.
        - Implement robust error handling and logging.
    4. Configurable Field Mapping:
        - Implement field mapping configurations through an external YAML file.
        - Ensure the mappings are easily adjustable without code changes.

#### Additional Notes:
- Default to the current date when no date is provided.
- Use predefined Pydantic models for `Transaction` and `ItemDetail` validation.
- You are provided with an example of the expected outputs.

Additionally, tests are provided in the `/tests` folder. Run them with the following command:

```
python -m pytest tests/test_data_transformation.py
```

### 2.  Develop a small Flask API for ERP Integration
You are tasked with developing a Flask-based API application that interacts with a legacy ERP system. The application will provide endpoints for fetching product information and finding the nearest technicians based on geographical coordinates. Additionally, you will need to calculate distances between locations using the Haversine formula.

- The project will be divided into two main functionalities to develop:

    - Product Information : `/api/product/` - An endpoint to fetch details like stock and status of a specific product from the legacy ERP.
    - Technician Location : `/api/technicians/nearest/` - An endpoint to return the two nearest technicians based on the given latitude and longitude.

- Requirements:
    - **Flask API:** You will create a Flask web application with two main routes.  The API will interact with the legacy ERP system by sending HTTP requests to retrieve data (such as stock availability and technician details).
    - **Product Information Endpoint (`/api/products`):** This endpoint will accept a `GET` request with a query parameter `part_id`. It will fetch the stock and status of the product associated with the given `part_id` from the legacy ERP system.
    - **Technician Information Endpoint (`/api/technicians/nearest`):** This endpoint will accept `GET` requests with latitude (`lat`) and longitude (`lon`) as query parameters.  It will return the two nearest technicians based on the geographical coordinates, using the Haversine formula for distance calculation.
    - **Error Handling:** You must handle cases where data from the ERP system is unavailable or incorrect input is provided (e.g., invalid latitude/longitude or no technicians found).
    - **Haversine Formula:** Implement the Haversine formula to calculate the distance between two geographical points (latitude/longitude).

- Old ERP endpoints example (you have part_id from 1 to 4 and their corresponding types as an example):
    - "https://cdn.nuwe.io/challenges-ds-datasets/hackathon-schneider-erp/parts/{part_id}"
        ```
        {
            "part_id":"1",
            "type":"A05",
            "status":"ok"
        }
        ```
    - "https://cdn.nuwe.io/challenges-ds-datasets/hackathon-schneider-erp/stock/{type}"
        ```
        {
            "type":"A05",
            "stock":76
        }
        ```
    - "https://cdn.nuwe.io/challenges-ds-datasets/hackathon-schneider-erp/technicians/available"
        ```
        [{
            "id":"1",
            "name": "Ian",
            "latitude": 48.56181,
            "longitude": 43.50553"
        }]
        ```

#### API Endpoints

| **Endpoint**               | **HTTP Method** | **Request Body**                 | **Response**                                        | **Status Codes**                                  |
|----------------------------|-----------------|----------------------------------|-----------------------------------------------------|---------------------------------------------------|
| `/api/product`             | GET             |`{ "part_id": int}`               | `{"id" int, "type":str, "stock" : int , "status" : str}` | 200 Success, 400 Bad Request,  500 Internal Error |
| `/api/technicians/nearest` | GET             | `{ "lon": float, "lat" : float}` | `{"id": int, "name": str, "distance_km": float}`    | 200 Success, 400 Bad Request, 500 Internal Error  |
 

You may test your solution running the following commands:

```
python api_rest/main.py & 
python -m pytest tests/test_api.py
```

### 3.  Python Algorithms
You are tasked with developing the following two algorithms:
    
1. Given a string, return the first non-repeating character. If there is no such character, return an empty string.
Character comparisons are case-insensitive (e.g. 'A' and 'a' are considered the same), but you should return the character in its original case as it appears in the input string.

**Examples:**
    string = 'submission' -> return 'u'
    string = 'nnn' -> return ''
    string = 'SUbMission' -> return 'U'

2. Given an integer (num), return a list containing two values:
- The total number of unique numbers that are divisible by 3, formed from the combinations of the digits of num.
- From the combinations, the maximum number divisible by 3.
- Note:
    - 0 is excluded from the count.
    - The numbers must be formed from the digits of `num` and the combinations can have different lengths.
    - If there is no number that has all the properties, return [0, None]

**Example:**
    num = 39 -> return [4, 93] . All possible numbers are 3,9,39,93 , as all of them are multiples of 3, the total number of multiples is 4 and the maximum number is 93.
    num = 330 -> return [5, 330] . The numbers are 3,30,33,303,330 , as all of them are multiples of 3, the total number of multiples is 5 and the maximum number is 330.
    num = 23 -> return [1, 3] . The numbers are 2,3,23,32. The only number multiple of 3 in this case is 3 itself.


You may test your algorithms running the following command:

```
python -m pytest tests/test_algorithms.py
```

### 4. SQL Queries Task
    
You are provided with a .sql file to set up the databases. Your task is to implement the required functions that will generate the specified tables and outputs. All results should be **rounded to two decimal places** when needed.
The initial script is given in `sql_queries/solution.py`, where you will complete the functions.

To setup de database, run the following command in the terminal:

```
python sql_queries/setup_database.py
```

#### 1. Top selling products
Return the 3 top performing products for each category, based on the number of items sold. Store the results within a new table named "TopSellingProducts" and round all numeric fields to 2 decimals where applicable. Your function should overwrite the table on each execution to ensure data is current.
Create a new table in the database schema named "TopSellingProducts" with the top 3 selling products in each category.

**Table Schema:**

| category (text) | name (text)  | total_sales (real) | sales_rank (int) |
|-----------------|--------------|--------------------|------------------|
|-----------------|--------------|--------------------|------------------|

#### 2. Late deliveries:
The company has a policy of 5 days delivery maximum. Return the percentage of deliveries that were delivered late (only from the "Delivered" packages).
- Calculate the percentage of "Delivered" packages that were late (delivered in more than 5 days).
- Return the result rounded to 2 decimals.


#### 3. Customer Sales performance. 
Flag each customer as  "High-value Customer" when the customer's total revenue is higher than the average total revenue among all customers. Else the customer's category should be set as "Regular Customer". Get the total orders and total revenue for each customer as well as their revenue rank.
Create a new table in the database schema named "CustomerSalesPerformance" with the following schema:


| customer_id (int) | total_orders (int) | total_revenue (real) | avg_order_value (real) | revenue_rank (int) | customer_category (text) |
|-------------------|--------------------|----------------------|------------------------|--------------------|--------------------------|
|-------------------|--------------------|----------------------|------------------------|--------------------|--------------------------|

      
4. Inventory Sales Forecast
    Create a new table in the database schema named "SalesForecast". Based on the last 3 months of purchases, estimate the months before stockout for each product and rank the products based on their stock.

| product_id (int) | product_name (text) | stock_quantity (int) | sales_last_3_months (int) | estimated_months_before_stockout (int) | stock_rank (int) |
|------------------|---------------------|----------------------|---------------------------|----------------------------------------|------------------|
|------------------|---------------------|----------------------|---------------------------|----------------------------------------|------------------|

5. Order Profitability and Discount Analysis
    Create a new table in the database schema named "DiscountAnalysis" to provide a summary of the discounts applied per order and the profit obtained. Also rank each order by its profit.
    

| order_id (int) | total_revenue (real) | total_cost (real) | profit (real) | profit_margin_percentage (real) | discount_percentage (real) | profitability_rank (int) |
|----------------|----------------------|-------------------|---------------|---------------------------------|----------------------------|--------------------------|
|----------------|----------------------|-------------------|---------------|---------------------------------|----------------------------|--------------------------|


You may test your functions running the following command:

```
python -m pytest tests/test_sql.py
```


### 5. Basic Logic Questions
Return the answer of the following questions in the file `questions/answers.json`. Maintain the given format of the file, you can manually change the value in the given file example.

1. A factory produces 20 widgets per hour during an 8-hour shift. However, every 13th widget is defective and must be discarded. How many acceptable widgets are produced in one shift?
2. A retail  store runs a "buy 2, get 1 free" promotion. If a customer selects 9 identical items, how many do they actually pay for?
3. An online store processed 150 orders per hour. Due to a temporary system glitch, 10% of orders are not processed correctly. In a 4-hour period, how many orders are processed correctly?
4. A company's profit margin increases by 2% per month, compounded monthly. If the initial margin is 10%, what is the profit margin after 3 months (rounded to two decimal places)?
5. A project has three tasks. Task A takes 30 minutes and must be completed before Tasks B and C can begin. Task B takes 45 minutes, and Task C takes 20 minutes. (Tasks B and C run concurrently once A is finished.). What is the minimum total time to complete the project?
6. A financial ledger should balance to zero. If the current recorded transactions show a total credit of 150€, what is the amount of the missing debit transactions?
7. A department's budget is increased by 10% in one quarter. If the initial budget is 10000€. What is the new budget after the increase?
8. In a quality control process, 60% of products pass inspection on the first try. The remaining products are re-inspected, with an 80% pass rate on the second attempt. What percentage of the total products pass quality control after both inspections?
9. A warehouse starts the month with 500 units of inventory. During the month, 400 units are sold, and 5% of the starting inventory is lost to shrinkage. How many units remain at month's end?
10. A support team resolves 12 tickets per day but receives 18 new tickets daily. Any unresolved tickets roll over to the next day. After 3 days, how many tickets remain unresolved?

### ✅ How to Test
Example test cases are provided in the `tests/` folder. The example command for the algorithm tasks is the following:
```
python -m pytest tests/test_algorithms.py
```
Although some basic tests are provided, you are encouraged to implement your own tests for additional scenarios.

- **Please note:**
The actual tests used for evaluation will differ and will not be shared in advance.


## 📤 Submission
To successfully submit your solution, follow these steps:

1. Complete the proposed tasks and add all the necessary libraries in the `requirements.txt` file.
2. Continuously push your changes as you work.
3. Monitor your progress and wait for the results, it may take up to a few minutes.
4. Once satisfied with your solution, click the "Submit Challenge" button.



## 📊 Evaluation

The final score will be given according to whether or not the objectives have been met.

In this case, the challenge will be evaluated on 1500 points which are distributed as follows:

- Task 1: 300 points
- Task 2: 300 points
- Task 3: 300 points
- Task 4: 300 points
- Task 5: 300 points

## ❓ Additional information

**Q1: Can I add resources that are not in requirements.txt?**

A1: Yes, new resources have to be added if necessary. Remember to add them to the `requirements.txt` file.

**Q2: Can I change the given project structure or rename the files?**

A2: No, you should not change the given project structure as the given format is necessary for the correction.

