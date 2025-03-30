from flask import Flask, jsonify, request
import requests
from haversine import haversine as calculate_distance
import math


# Legacy ERP API Base URL
LEGACY_ERP_BASE_URL = (
    "https://cdn.nuwe.io/challenges-ds-datasets/hackathon-schneider-erp"
)
app = Flask(__name__)

@app.route("/api/products", methods=["GET"])
def get_product():
    part_id = request.args.get('part_id')
    if not part_id or not part_id.isdigit():
        return jsonify({"error": "Invalid part_id"}), 400

    try:
        product_response = requests.get(f'{LEGACY_ERP_BASE_URL}/parts/{part_id}')
        product_response.raise_for_status()
        product_data = product_response.json()

        stock_response = requests.get(f'{LEGACY_ERP_BASE_URL}/stock/{product_data["type"]}')
        stock_response.raise_for_status()
        stock_data = stock_response.json()

        return jsonify({
            "id": int(part_id),
            "type": product_data["type"],
            "stock": stock_data["stock"],
            "status": product_data["status"]
        }), 200
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500
    except KeyError as e:
        return jsonify({"error": f"Missing key in response: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

# Haversine formula to calculate the great-circle distance between two points
def haversine(lat1, lon1, lat2, lon2):
    pos_1 = (lat1, lon1) # (lat, lon)
    pos_2 = (lat2, lon2)

    distance = calculate_distance(pos_1, pos_2)

    # Multiply by 1000 to work with the third decimal place
    scaled_value = distance * 1000
    decimal_part = scaled_value % 10  # Get the third decimal place

    # If the third decimal is greater than or equal to 6, round up
    if decimal_part >= 6:
        return round(distance, 2)
    else:
        # Truncate to 2 decimal places without rounding
        return math.floor(distance * 100) / 100

@app.route("/api/technicians/nearest", methods=["GET"])
def get_nearest_technicians():
    try:
        lat = float(request.args.get('lat'))
        lon = float(request.args.get('lon'))
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid latitude or longitude"}), 400

    try:
        response = requests.get(f'{LEGACY_ERP_BASE_URL}/technicians/available')
        response.raise_for_status()
        technicians = response.json()

        # Handle empty technician list
        if not technicians:
            return jsonify({"error": "No technicians available"}), 500

        technicians = sorted(technicians, key=lambda x: haversine(lat, lon, float(x["latitude"]), float(x["longitude"])))
        nearest_technicians = technicians[:2]

        result = [{
            "id": int(t["id"]),
            "name": t["name"],
            "distance_km": haversine(lat, lon, float(t["latitude"]), float(t["longitude"]))
        } for t in nearest_technicians]

        return jsonify(result), 200
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500
    except KeyError as e:
        return jsonify({"error": f"Missing key in response: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=3000)
