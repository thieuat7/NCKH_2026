import requests
import time

url = "http://127.0.0.1:8000/predict"  # Thay bằng URL API thực tế

data = [
  {"transaction_id":"TXN100000001","user_id":"294828221","receiver_id":"824829232","timestamp":"2025-09-16T01:12:45Z","transaction_amount":250000,"transaction_type":"transfer","transaction_description":"Chuyen tien","device_id":"DEV-101-54321","account_balance_before_txn":5000000},
  {"transaction_id":"TXN100000002","user_id":"294828221","receiver_id":"724829233","timestamp":"2025-09-16T03:25:10Z","transaction_amount":120000,"transaction_type":"transfer","transaction_description":"Chuyen tien","device_id":"DEV-102-12345","account_balance_before_txn":3500000},
  {"transaction_id":"TXN100000003","user_id":"294828221","receiver_id":"624829234","timestamp":"2025-09-16T04:40:22Z","transaction_amount":500000,"transaction_type":"transfer","transaction_description":"Chuyen tien","device_id":"DEV-103-23456","account_balance_before_txn":7000000},
  {"transaction_id":"TXN100000004","user_id":"294828221","receiver_id":"524829235","timestamp":"2025-09-16T06:55:11Z","transaction_amount":75000,"transaction_type":"transfer","transaction_description":"Chuyen tien","device_id":"DEV-104-34567","account_balance_before_txn":1000000},
  {"transaction_id":"TXN100000005","user_id":"294828221","receiver_id":"424829236","timestamp":"2025-09-16T08:12:34Z","transaction_amount":320000,"transaction_type":"transfer","transaction_description":"Chuyen tien","device_id":"DEV-105-45678","account_balance_before_txn":1500000},
  {"transaction_id":"TXN100000006","user_id":"294828221","receiver_id":"324829237","timestamp":"2025-09-16T09:30:00Z","transaction_amount":180000,"transaction_type":"transfer","transaction_description":"Chuyen tien","device_id":"DEV-106-56789","account_balance_before_txn":2500000},
  {"transaction_id":"TXN100000007","user_id":"294828221","receiver_id":"224829238","timestamp":"2025-09-16T10:45:50Z","transaction_amount":90000,"transaction_type":"transfer","transaction_description":"Chuyen tien","device_id":"DEV-107-67890","account_balance_before_txn":1200000},
  {"transaction_id":"TXN100000008","user_id":"294828221","receiver_id":"124829239","timestamp":"2025-09-16T12:10:12Z","transaction_amount":450000,"transaction_type":"transfer","transaction_description":"Chuyen tien","device_id":"DEV-108-78901","account_balance_before_txn":6000000},
  {"transaction_id":"TXN100000009","user_id":"294828221","receiver_id":"924829240","timestamp":"2025-09-16T13:25:44Z","transaction_amount":220000,"transaction_type":"transfer","transaction_description":"Chuyen tien","device_id":"DEV-109-89012","account_balance_before_txn":4000000},
  {"transaction_id":"TXN100000010","user_id":"294828221","receiver_id":"824829241","timestamp":"2025-09-16T14:40:33Z","transaction_amount":600000,"transaction_type":"transfer","transaction_description":"Chuyen tien","device_id":"DEV-110-90123","account_balance_before_txn":8000000},
  {"transaction_id":"TXN100000011","user_id":"294828221","receiver_id":"724829242","timestamp":"2025-09-16T15:55:11Z","transaction_amount":100000,"transaction_type":"transfer","transaction_description":"Chuyen tien","device_id":"DEV-111-01234","account_balance_before_txn":1500000},
  {"transaction_id":"TXN100000012","user_id":"294828221","receiver_id":"624829243","timestamp":"2025-09-16T16:10:50Z","transaction_amount":350000,"transaction_type":"transfer","transaction_description":"Chuyen tien","device_id":"DEV-112-12345","account_balance_before_txn":4500000},
  {"transaction_id":"TXN100000013","user_id":"294828221","receiver_id":"524829244","timestamp":"2025-09-16T17:25:05Z","transaction_amount":270000,"transaction_type":"transfer","transaction_description":"Chuyen tien","device_id":"DEV-113-23456","account_balance_before_txn":3200000},
  {"transaction_id":"TXN100000014","user_id":"294828221","receiver_id":"424829245","timestamp":"2025-09-16T18:40:22Z","transaction_amount":50000,"transaction_type":"transfer","transaction_description":"Chuyen tien","device_id":"DEV-114-34567","account_balance_before_txn":800000},
  {"transaction_id":"TXN100000015","user_id":"294828221","receiver_id":"324829246","timestamp":"2025-09-16T19:55:11Z","transaction_amount":900000,"transaction_type":"transfer","transaction_description":"Chuyen tien","device_id":"DEV-115-45678","account_balance_before_txn":10000000},
  {"transaction_id":"TXN100000016","user_id":"294828221","receiver_id":"224829247","timestamp":"2025-09-16T20:10:45Z","transaction_amount":150000,"transaction_type":"transfer","transaction_description":"Chuyen tien","device_id":"DEV-116-56789","account_balance_before_txn":2000000},
  {"transaction_id":"TXN100000017","user_id":"294828221","receiver_id":"124829248","timestamp":"2025-09-16T21:25:33Z","transaction_amount":420000,"transaction_type":"transfer","transaction_description":"Chuyen tien","device_id":"DEV-117-67890","account_balance_before_txn":5500000},
  {"transaction_id":"TXN100000018","user_id":"294828221","receiver_id":"924829249","timestamp":"2025-09-16T22:40:12Z","transaction_amount":310000,"transaction_type":"transfer","transaction_description":"Chuyen tien","device_id":"DEV-118-78901","account_balance_before_txn":4000000},
  {"transaction_id":"TXN100000019","user_id":"294828221","receiver_id":"824829250","timestamp":"2025-09-16T23:55:00Z","transaction_amount":60000,"transaction_type":"transfer","transaction_description":"Chuyen tien","device_id":"DEV-119-89012","account_balance_before_txn":900000},
  {"transaction_id":"TXN100000020","user_id":"294828221","receiver_id":"724829251","timestamp":"2025-09-16T00:15:22Z","transaction_amount":500000,"transaction_type":"transfer","transaction_description":"Chuyen tien","device_id":"DEV-120-90123","account_balance_before_txn":7000000},
  {"transaction_id":"TXN100000021","user_id":"294828221","receiver_id":"624829252","timestamp":"2025-09-16T01:30:44Z","transaction_amount":200000,"transaction_type":"transfer","transaction_description":"Chuyen tien","device_id":"DEV-121-01234","account_balance_before_txn":3500000},
  {"transaction_id":"TXN100000022","user_id":"294828221","receiver_id":"524829253","timestamp":"2025-09-16T02:45:33Z","transaction_amount":125000,"transaction_type":"transfer","transaction_description":"Chuyen tien","device_id":"DEV-122-12345","account_balance_before_txn":2500000},
  {"transaction_id":"TXN100000023","user_id":"294828221","receiver_id":"424829254","timestamp":"2025-09-16T03:55:11Z","transaction_amount":80000,"transaction_type":"transfer","transaction_description":"Chuyen tien","device_id":"DEV-123-23456","account_balance_before_txn":1200000},
  {"transaction_id":"TXN100000024","user_id":"294828221","receiver_id":"324829255","timestamp":"2025-09-16T04:10:22Z","transaction_amount":330000,"transaction_type":"transfer","transaction_description":"Chuyen tien","device_id":"DEV-124-34567","account_balance_before_txn":4000000},
  {"transaction_id":"TXN100000025","user_id":"294828221","receiver_id":"224829256","timestamp":"2025-09-16T05:25:33Z","transaction_amount":270000,"transaction_type":"transfer","transaction_description":"Chuyen tien","device_id":"DEV-125-45678","account_balance_before_txn":3200000},
  {"transaction_id":"TXN100000026","user_id":"294828221","receiver_id":"124829257","timestamp":"2025-09-16T06:40:44Z","transaction_amount":400000,"transaction_type":"transfer","transaction_description":"Chuyen tien","device_id":"DEV-126-56789","account_balance_before_txn":5000000},
  {"transaction_id":"TXN100000027","user_id":"294828221","receiver_id":"924829258","timestamp":"2025-09-16T07:55:11Z","transaction_amount":60000,"transaction_type":"transfer","transaction_description":"Chuyen tien","device_id":"DEV-127-67890","account_balance_before_txn":900000},
  {"transaction_id":"TXN100000028","user_id":"294828221","receiver_id":"824829259","timestamp":"2025-09-16T09:10:22Z","transaction_amount":150000,"transaction_type":"transfer","transaction_description":"Chuyen tien","device_id":"DEV-128-78901","account_balance_before_txn":2000000},
  {"transaction_id":"TXN100000029","user_id":"294828221","receiver_id":"724829260","timestamp":"2025-09-16T10:25:33Z","transaction_amount":500000,"transaction_type":"transfer","transaction_description":"Chuyen tien","device_id":"DEV-129-89012","account_balance_before_txn":7000000},
  {"transaction_id":"TXN100000030","user_id":"294828221","receiver_id":"624829261","timestamp":"2025-09-16T11:40:44Z","transaction_amount":320000,"transaction_type":"transfer","transaction_description":"Chuyen tien","device_id":"DEV-130-90123","account_balance_before_txn":4000000}
]




for txn in data:
    try:
        response = requests.post(url, json=txn)
        print(f"Status: {response.status_code}")
        try:
            print("Response:", response.json())
        except Exception:
            print("Response (raw):", response.text)
    except Exception as e:
        print(f"Error: {e}")
    time.sleep(5)
