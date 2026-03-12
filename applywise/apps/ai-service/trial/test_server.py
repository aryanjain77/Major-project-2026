import requests
import sys

print("Testing backend connection...")
print("-" * 50)

try:
    # Test root endpoint
    response = requests.get('http://localhost:5000/', timeout=5)
    print(f"✅ Root endpoint: {response.status_code}")
    print(f"   Response: {response.json()}")
except requests.exceptions.ConnectionRefusedError:
    print("❌ Connection refused - Backend is not running!")
    sys.exit(1)
except requests.exceptions.Timeout:
    print("❌ Request timed out - Backend is not responding!")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)

try:
    # Test popular roles endpoint
    response = requests.get('http://localhost:5000/api/roadmap/popular-roles', timeout=5)
    print(f"✅ Popular roles endpoint: {response.status_code}")
    data = response.json()
    print(f"   Found {len(data.get('roles', []))} roles")
except Exception as e:
    print(f"❌ Popular roles endpoint failed: {e}")

print("-" * 50)
print("✅ Backend is working correctly!")