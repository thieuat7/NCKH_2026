
````markdown
# Fraud Detection LSTM API

## Mô tả
Dự án này xây dựng một **API phát hiện gian lận giao dịch tài chính** sử dụng **mô hình LSTM Autoencoder**.  
API nhận dữ liệu giao dịch, xử lý đặc trưng, dự đoán mức độ bất thường và trả về kết quả.

---

## Yêu cầu hệ thống
- Python 3.12 trở lên  
- Các thư viện được liệt kê trong [requirements.txt](requirements.txt)

---

## Cài đặt

1. **Clone dự án**
```bash
git clone <repo_url>
cd <project_folder>
````

2. **Tạo môi trường ảo và cài đặt thư viện**

```bash
python -m venv venv      # Tạo môi trường ảo
# Kích hoạt môi trường:
# Windows
venv\Scripts\activate
# Linux / Mac
source venv/bin/activate

pip install -r requirements.txt
```

3. **Chạy dự án**

```bash
uvicorn src.api.main:app --reload
```

* API sẽ chạy ở địa chỉ mặc định: `http://127.0.0.1:8000/predict`

---

## Sử dụng API

* Bạn có thể sử dụng **Postman** hoặc bất kỳ công cụ gửi HTTP request nào để test API.

* **Dữ liệu mẫu (POST request JSON):**

```json
{
  "transaction_id": "TXN100000001", 
  "user_id": "294828222",
  "receiver_id": "524829262",
  "timestamp": "2025-09-16T12:55:10Z",
  "transaction_amount": 210000,
  "transaction_type": "transfer",
  "transaction_description": "Chuyen tien",
  "device_id": "DEV-131-01234",
  "account_balance_before_txn": 4500000
}
```

---

## Kết quả trả về

API sẽ trả về **dạng JSON** với thông tin về giao dịch và mức độ bất thường.
Ví dụ:

```json
{
    "statusCode": 200,
    "error": null,
    "message": "CALL API SUCCESS",
    "data": {
        "percent": 25.285001754760742
    }
}
```

---

## Ghi chú

* Luôn sử dụng **môi trường ảo** để tránh xung đột thư viện.
* Cập nhật `requirements.txt` nếu thêm thư viện mới.
