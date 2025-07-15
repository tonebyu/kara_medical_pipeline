import requests

BASE_URL = "http://127.0.0.1:8000"

def test_root():
    response = requests.get(f"{BASE_URL}/")
    print("[/] Root:", response.status_code, response.json())

def test_top_products(limit=5):
    response = requests.get(f"{BASE_URL}/api/reports/top-products?limit={limit}")
    print(f"[GET] /api/reports/top-products?limit={limit} -> {response.status_code}")
    for item in response.json():
        print("  ", item)

def test_channel_activity(channel_name="MOH_Channel"):
    response = requests.get(f"{BASE_URL}/api/channels/{channel_name}/activity")
    print(f"[GET] /api/channels/{channel_name}/activity -> {response.status_code}")
    print("  ", response.json() if response.ok else response.text)

def test_search_messages(query="paracetamol"):
    response = requests.get(f"{BASE_URL}/api/search/messages?query={query}")
    print(f"[GET] /api/search/messages?query={query} -> {response.status_code}")
    results = response.json()
    print(f"  Found {len(results)} messages.")
    for msg in results[:5]:  # Show first 5
        print("   -", msg["content"][:80])

if __name__ == "__main__":
    print("Running Kara API Endpoint Tests...\n")
    test_root()
    test_top_products()
    test_channel_activity("MOH_Channel")  # Replace with real channel name
    test_search_messages("paracetamol")   # Replace with actual keyword
