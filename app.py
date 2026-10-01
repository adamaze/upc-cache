import os
import requests
from flask import Flask

app = Flask(__name__)
CACHE_DIR = "/upc_cache"

os.makedirs(CACHE_DIR, exist_ok=True)

@app.route('/<upc>')
def lookup_upc(upc):
    cache_file = os.path.join(CACHE_DIR, f"{upc}.txt")

    # 1. Check local cache
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            return f"[CACHED] {f.read()}"

    # 2. Make the API call with a custom User-Agent
    url = f"https://world.openfoodfacts.org/api/v0/product/{upc}.json"
    headers = {"User-Agent": "SimpleUPCApp/1.0 - GitHubActionBuild"}
    response = requests.get(url, headers=headers)

    # 3. Handle errors safely
    if response.status_code != 200:
        return f"External API Error (Status {response.status_code})", 502

    try:
        data = response.json()
    except ValueError:
        return "External API Error: Did not receive valid JSON", 502

    # 4. Extract and save
    product = data.get("product", {})
    product_name = product.get("product_name")

    if product_name:
        with open(cache_file, "w") as f:
            f.write(product_name)
        return f"[API] {product_name}"
    else:
        return f"Product not found for UPC: {upc}", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
