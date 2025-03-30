import json
import yaml
import logging
from typing import List, Dict, Any, Optional, ClassVar
from pydantic import BaseModel, model_validator, field_validator
from datetime import date, datetime
from pathlib import Path
import time
import re
import csv

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ------------------------------
#     ConfigLoader Class
# ------------------------------


class ConfigLoader:
    """Loads and stores configuration from a YAML file."""

    def __init__(self, yaml_file: Path):
        try:
            with yaml_file.open("r", encoding="utf-8") as file:
                self.config = yaml.safe_load(file)
        except FileNotFoundError:
            logger.error(f"Configuration file not found: {yaml_file}")
            raise
        except yaml.YAMLError as e:
            logger.error(f"Error parsing YAML file: {e}")
            raise

    def get(self, key: str, default: Any = None) -> Any:
        """Retrieve a value from the config."""
        return self.config.get(key, default)

# ------------------------------
#        Pydantic Models
# ------------------------------

class Transaction(BaseModel):
    config: ClassVar[ConfigLoader] = None
    alias_map: ClassVar[Dict[str, List[str]]] = {}

    transaction_id: int
    customer_name: Optional[str] = "Unknown"
    purchase_date: Optional[date] = datetime.now().date()
    total_amount: float
    status: str

    @classmethod
    def set_config(cls, config: ConfigLoader):
        cls.config = config
        cls.alias_map = {
            "transaction_id": config.get("id_fields", []),
            "customer_name": config.get("name_fields", []),
            "purchase_date": config.get("date_fields", []),
            "total_amount": config.get("amount_fields", []),
            "status": config.get("status_fields", [])
        }

    @model_validator(mode="before")
    @classmethod
    def apply_aliases(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Apply aliases dynamically to map input data to model fields."""
        if not cls.alias_map:
            return values

        mapped_values = {}
        for field_name, aliases in cls.alias_map.items():
            for alias in aliases:
                if '.' in alias:
                    # Handle nested dictionary alias
                    nested_keys = alias.split('.')
                    nested_value = values
                    try:
                        for key in nested_keys:
                            nested_value = nested_value[key]
                        mapped_values[field_name] = nested_value
                        break  # Stop at the first valid nested alias
                    except (TypeError, KeyError):
                        continue  # Move on to the next alias
                elif alias in values:
                    mapped_values[field_name] = values[alias]
                    break  # Stop at the first matching alias

            # If no alias matched, retain the original field value if it exists
            if field_name not in mapped_values and field_name in values:
                mapped_values[field_name] = values[field_name]

        return mapped_values  

    # Implement Class atributes if needed
    @field_validator("transaction_id", "customer_name", "purchase_date", "total_amount", "status", mode="before")
    def unified_validator(cls, value, info):
        if value is None:
            logger.warning(f"Field '{info.field_name}' is None, defaulting to appropriate value.")
            if info.field_name == "transaction_id":
                return 0  # Default ID if missing
            if info.field_name == "customer_name":
                return "Unknown"
            if info.field_name == "purchase_date":
                return datetime.now().date()
            if info.field_name == "total_amount":
                return 0.0
            if info.field_name == "status":
                return "Unknown"

        # Handle dictionary input with possible aliases
        if isinstance(value, dict):
            aliases = cls.alias_map.get(info.field_name, [])
            for alias in aliases:
                if alias in value:
                    return value[alias]
            if info.field_name == "customer_name":
                first_name = value.get("first_name", "")
                last_name = value.get("last_name", "")
                return f"{first_name} {last_name}".strip()

        # Normalize transaction_id
        if info.field_name == "transaction_id":
            if isinstance(value, str):
                # Remove non-digit characters
                cleaned_value = re.sub(r'[^\d]', '', value.strip())
                if cleaned_value.isdigit():
                    return int(cleaned_value)
                raise ValueError(f"Invalid transaction ID: '{value}'")
            if isinstance(value, int):
                return value
            raise ValueError(f"Unsupported type for transaction ID: {type(value).__name__} with value: '{value}'")

        # Normalize customer_name
        if info.field_name == "customer_name" and isinstance(value, str):
            try:
                return re.sub(r'\s+', ' ', value.strip())
            except ValueError:
                raise ValueError(f"Unable to parse '{value}' as a str")

        # Normalize purchase_date
        if info.field_name == "purchase_date" and isinstance(value, str):
            date_formats = cls.config.get("date_formats", [])
            for fmt in date_formats:
                try:
                    return datetime.strptime(value, fmt).date()
                except ValueError:
                    continue
            raise ValueError(f"Unable to parse '{value}' as a date")

        # Parse total_amount
        if info.field_name == "total_amount" and isinstance(value, str):
            try:
                return format_price(value)
            except ValueError:
                raise ValueError(f"Unable to parse '{value}' as a float")

        # Map status values to standard form
        if info.field_name == "status" and isinstance(value, str):
            status_mapping = cls.config.get("status_mapping", {})
            for standard_status, variations in status_mapping.items():
                value = value.strip()
                if value in variations:
                    return standard_status
            return value

        return value

class ItemDetail(BaseModel):
    details_id: int
    transaction_id: int
    item: str
    quantity: int
    price: float

    # Implement Class atributes if needed

    @classmethod
    def set_config(cls, config: ConfigLoader):
        cls.config = config
        cls.alias_map = {
            "details_id": config.get("details_id_fields", []),
            "transaction_id": config.get("transaction_id_fields", []),
            "item": config.get("item_fields", []),
            "quantity": config.get("quantity_fields", []),
            "price": config.get("price_fields", [])
        }

    @model_validator(mode="before")
    @classmethod
    def apply_aliases(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Apply aliases dynamically to map input data to model fields."""
        if not cls.alias_map:
            return values

        mapped_values = {}
        for field_name, aliases in cls.alias_map.items():
            for alias in aliases:
                if '.' in alias:
                    nested_keys = alias.split('.')
                    nested_value = values
                    try:
                        for key in nested_keys:
                            nested_value = nested_value[key]
                        mapped_values[field_name] = nested_value
                        break
                    except (TypeError, KeyError):
                        continue
                elif alias in values:
                    mapped_values[field_name] = values[alias]
                    break

            # Fallback: if no alias matched, use the direct field value if it exists
            if field_name not in mapped_values and field_name in values:
                mapped_values[field_name] = values[field_name]

        return mapped_values

    @field_validator("details_id", "transaction_id", "item", "quantity", "price", mode="before")
    def unified_validator(cls, value, info):
        if value is None:
            logger.warning(f"Field '{info.field_name}' is None, defaulting to appropriate value.")
            if info.field_name == "details_id":
                return 0
            if info.field_name == "transaction_id":
                return 0
            if info.field_name == "item":
                return "Unknown Item"
            if info.field_name == "quantity":
                return 1
            if info.field_name == "price":
                return 0.0

        # Validar `details_id` y `transaction_id`
        if info.field_name in ["details_id", "transaction_id"]:
            if isinstance(value, str):
                cleaned_value = re.sub(r'[^\d]', '', value.strip())
                if cleaned_value.isdigit():
                    return int(cleaned_value)
                logger.warning(f"Invalid ID for '{info.field_name}': '{value}', defaulting to 0")
                return 0
            if isinstance(value, int):
                return value

        # Validar `item`
        if info.field_name == "item":
            if isinstance(value, str):
                return value.strip()
            logger.warning(f"Invalid item name: '{value}', defaulting to 'Unknown Item'")
            return "Unknown Item"

        # Validar `quantity`
        if info.field_name == "quantity":
            try:
                return int(value)
            except (ValueError, TypeError):
                logger.warning(f"Invalid quantity: '{value}', defaulting to 1")
                return 1

        # Validar `price`
        if info.field_name == "price":
            try:
                return format_price(value)
            except ValueError:
                logger.warning(f"Invalid price: '{value}', defaulting to 0.0")
                return 0.0

        return value

def format_price(value: Any) -> float:
    """
    Format price to two decimal places and remove trailing zeros.
    Detects the most likely decimal separator.
    Returns 0.0 if unable to parse the input.
    """
    try:
        # Convert directly if it's already a float or int
        if isinstance(value, (float, int)):
            return round(float(value), 2)

        # Convert from string representation
        if isinstance(value, str):
            # Remove any non-digit and non-dot/comma characters
            value = re.sub(r"[^\d,\.]", "", value)
            
            # Identify the last occurrence of dot and comma
            last_dot = value.rfind('.')
            last_comma = value.rfind(',')

            # Determine which one is the decimal separator (whichever comes last)
            if last_dot > last_comma:
                # Dot is the decimal separator, remove commas (thousand separators)
                value = value.replace(',', '')
            elif last_comma > last_dot:
                # Comma is the decimal separator, remove dots (thousand separators)
                value = value.replace('.', '').replace(',', '.')
            elif last_comma == last_dot == -1:
                # No dot or comma found, return as a plain number
                return float(value)

            return round(float(value), 2)

    except (ValueError, TypeError):
        logger.warning(f"Unable to parse '{value}' as a float. Defaulting to 0.0")
        return 0.0  # Return a default value on failure

    # In case none of the above worked, return 0.0 as a fallback
    return 0.0

def parse_json_to_csv(
    json_data: List[Dict[str, Any]],
    transaction_file: Path,
    detail_file: Path,
    config: ConfigLoader,
):
    pass  # To implement

    Transaction.set_config(config)
    ItemDetail.set_config(config)

    transaction_file.parent.mkdir(parents=True, exist_ok=True)
    detail_file.parent.mkdir(parents=True, exist_ok=True)

    transaction_fields = config.get("transaction_fields", ["transaction_id", "customer_name", "purchase_date", "total_amount", "status"])
    detail_fields = config.get("detail_fields", ["details_id", "transaction_id", "item", "quantity", "price"])

    details_id_counter = 1

    with transaction_file.open("w", newline="", encoding="utf-8") as tf, detail_file.open("w", newline="", encoding="utf-8") as df:
        transaction_writer = csv.DictWriter(tf, fieldnames=transaction_fields)
        detail_writer = csv.DictWriter(df, fieldnames=detail_fields)

        transaction_writer.writeheader()
        detail_writer.writeheader()

        # Set to store unique transaction data
        written_transactions = set()

        for record in json_data:
            transaction = Transaction(**record)
            transaction_data = transaction.model_dump()

            # Convert the transaction data to a tuple for storing in the set
            transaction_tuple = tuple((k, v) for k, v in transaction_data.items() if k not in {"transaction_id", "customer_name"})

            # Avoid duplicated rows
            if transaction_tuple not in written_transactions:
                transaction_writer.writerow(transaction_data)
                written_transactions.add(transaction_tuple)

                details = record.get("items", [])
                for detail in details:
                    detail = ItemDetail(**detail, details_id=details_id_counter, transaction_id=transaction.transaction_id)
                    detail_data = detail.model_dump()
                    detail_writer.writerow(detail_data)

                    details_id_counter += 1

def process_single_file(filename: Path, transaction_file: Path, details_file: Path, config: ConfigLoader):
    with filename.open("r", encoding="utf-8") as file:
        json_data = json.load(file)

    parse_json_to_csv(json_data, transaction_file, details_file, config)

if __name__ == "__main__":
    start = time.time()

    # ------------------------------
    #      Load Configuration
    # ------------------------------

    config = ConfigLoader(Path("data_transformation/config.yml"))
    Transaction.set_config(config)
    ItemDetail.set_config(config)

    input_files = config.get("files", {}).get("input", [])
    output_file = Path(
        config.get("files", {}).get("transaction_output", "transactions.csv")
    )
    details_file = Path(config.get("files", {}).get("details_output", "details.csv"))

    if isinstance(input_files, str):
        input_files = [input_files]  # Wrap single file in a list if input is a string

    for filename in input_files:
        process_single_file(Path(filename), output_file, details_file, config)
