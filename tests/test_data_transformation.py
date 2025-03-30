from pathlib import Path
from datetime import date, datetime
import os

from data_transformation.main import (
    ConfigLoader,
    Transaction,
    ItemDetail,
    parse_json_to_csv,
)

data_path = "data_transformation/inputs/records.json"
config_path = "data_transformation/config.yml"
output_path = "data_transformation/outputs"

if os.path.exists("data_transformation/outputs/details_test_1.csv"):
    os.remove("data_transformation/outputs/details_test_1.csv")
if os.path.exists("data_transformation/outputs/transactions_test_1.csv"):
    os.remove("data_transformation/outputs/transactions_test_1.csv")


def test_config_loader_loads_file():
    config = ConfigLoader(Path(config_path))
    assert isinstance(config.config, dict)


def test_status_mapping_in_config():
    config = ConfigLoader(Path(config_path))
    status_mapping = config.get("status_mapping")
    assert "Completed" in status_mapping
    assert "Pending" in status_mapping


def test_transaction_model_valid_data():
    config = ConfigLoader(Path(config_path))

    Transaction.set_config(config)
    txn = Transaction(
        transaction_id=1,
        customer_name=" John  Doe ",
        purchase_date="2024-01-10",
        total_amount="1,200.50€",
        status="Completed",
    )
    assert txn.transaction_id == 1
    assert txn.customer_name == "John Doe"
    assert txn.purchase_date == date(2024, 1, 10)
    assert txn.total_amount == 1200.50
    assert txn.status == "Completed"


def test_item_detail_model_valid():
    config = ConfigLoader(Path(config_path))
    ItemDetail.set_config(config)
    item = ItemDetail(
        details_id=1, transaction_id=100, item="Laptop", quantity=1, price=1300.50
    )
    assert item.details_id == 1
    assert item.item == "Laptop"
    assert item.quantity == 1
    assert item.price == 1300.50


def test_parse_json_to_csv_outputs_transactions():
    sample_json = [
        {
            "id": "011",
            "customer": "Joe Doe",
            "purchase_date": "2024-01-10",
            "total_amount": "1,200.50€",
            "items": [{"item": "Laptop", "quantity": 1, "price": "1200.50"}],
            "status": "Completed",
        }
    ]

    transaction_file = Path(f"{output_path}/transactions_test_1.csv")
    details_file = Path(f"{output_path}/details_test_1.csv")
    config = ConfigLoader(Path(config_path))
    parse_json_to_csv(sample_json, transaction_file, details_file, config)

    assert transaction_file.exists(), "Transaction file not found"
    assert details_file.exists(), "Details file not found"

    # Validate transactions CSV
    with transaction_file.open("r") as f:
        lines = [line.strip() for line in f.readlines()]
        assert len(lines) == 2, "Different number of lines than expected"

        header = lines[0]
        data = lines[1]

        expected_header = (
            "transaction_id,customer_name,purchase_date,total_amount,status"
        )
        expected_data = "11,Joe Doe,2024-01-10,1200.5,Completed"

        assert header == expected_header, "Transaction header mismatch."
        assert data == expected_data, "Transaction data mismatch."

    # Validate details CSV
    with details_file.open("r") as f:
        lines = [line.strip() for line in f.readlines()]
        assert len(lines) == 2, "Different number of lines than expected"

        header = lines[0]
        data = lines[1]

        expected_header = "details_id,transaction_id,item,quantity,price"
        expected_data = "1,11,Laptop,1,1200.5"

        assert header == expected_header, "Details header mismatch"
        assert data == expected_data, "Details data mismatch"

def test_transaction_model_composed_name_valid_data():
    config = ConfigLoader(Path(config_path))

    Transaction.set_config(config)
    txn = Transaction(
        transaction_id=2,
        customer_name={"first_name": "Jane", "last_name": "Smith"},
        purchase_date="10/02/24",
        total_amount="950.00",
        status="Paid"
    )
    assert txn.transaction_id == 2
    assert txn.customer_name == "Jane Smith"
    assert txn.purchase_date == datetime(2024, 2, 10).date()
    assert txn.total_amount == 950
    assert txn.status == "Completed"

def test_transaction_model_complex_customer_name_valid_data():
    config = ConfigLoader(Path(config_path))

    Transaction.set_config(config)
    txn = Transaction(
        transaction_id=1,
        client={
            "first_name": "Jane",
            "last_name": "Smith"
        },
        purchase_date="2024-01-10",
        total_amount="1,200.50€",
        status="Completed",
    )
    assert txn.transaction_id == 1
    assert txn.customer_name == "Jane Smith"
    assert txn.purchase_date == date(2024, 1, 10)
    assert txn.total_amount == 1200.50
    assert txn.status == "Completed"

def test_transaction_model_buyer_full_name_valid_data():
    config = ConfigLoader(Path(config_path))

    Transaction.set_config(config)
    txn = Transaction(
        transaction_id=1,
        buyer={
            "full_name": "Alice    Brown"
        },
        purchase_date="2024-01-10",
        total_amount="1,200.50€",
        status="Completed",
    )
    assert txn.transaction_id == 1
    assert txn.customer_name == "Alice Brown"
    assert txn.purchase_date == date(2024, 1, 10)
    assert txn.total_amount == 1200.50
    assert txn.status == "Completed"

def test_item_detail_qty_model_valid():
    config = ConfigLoader(Path(config_path))
    ItemDetail.set_config(config)
    item = ItemDetail(
        details_id=1, transaction_id=100, item="Laptop", qty=1, price=1300.50
    )
    assert item.details_id == 1
    assert item.item == "Laptop"
    assert item.quantity == 1
    assert item.price == 1300.50

def test_transaction_model_special_amount_valid_data():
    config = ConfigLoader(Path(config_path))

    Transaction.set_config(config)
    txn = Transaction(
        transaction_id=1,
        customer_name=" John  Doe ",
        purchase_date="2024-01-10",
        total_amount="1 250.50 EUR",
        status="Completed",
    )
    assert txn.transaction_id == 1
    assert txn.customer_name == "John Doe"
    assert txn.purchase_date == date(2024, 1, 10)
    assert txn.total_amount == 1250.50
    assert txn.status == "Completed"

def test_transaction_model_problem_costs_format_valid_data():
    config = ConfigLoader(Path(config_path))

    Transaction.set_config(config)
    txn = Transaction(
        transaction_id=1,
        customer_name=" John  Doe ",
        purchase_date="2024-01-10",
        total_amount="€1.500,75",
        status="Completed",
    )
    assert txn.transaction_id == 1
    assert txn.customer_name == "John Doe"
    assert txn.purchase_date == date(2024, 1, 10)
    assert txn.total_amount == 1500.75
    assert txn.status == "Completed"