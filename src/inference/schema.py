from pydantic import BaseModel
from typing import Any, Optional
import numpy as np
from datetime import datetime

class PredictionRequest(BaseModel):
	# Định nghĩa cấu trúc dữ liệu đầu vào cho mô hình
	transaction_id: str
	user_id: str
	receiver_id: str
	transaction_amount: float
	timestamp: datetime 
	transaction_type: str
	transaction_description: str = None
	device_id: str = None
	account_balance_before_txn: float = None

class PredictionData(BaseModel):
    percent: float

class PredictionResponse(BaseModel):
    statusCode: int = 200
    error: Optional[str] = None
    message: str
    data: PredictionData
