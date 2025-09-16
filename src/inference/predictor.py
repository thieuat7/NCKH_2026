import os
import joblib
import numpy as np
from src.inference.schema import PredictionRequest, PredictionResponse
from src.inference.transaction_feature_engineering import add_transaction_and_enrich
from src.training.train_LSTM import train_models

csv_path = ""

def preprocess_input(request: PredictionRequest):
	# Chuyển dữ liệu đầu vào thành mảng numpy phù hợp với model
	# Nếu model cần encode type, cần xử lý thêm
	import pandas as pd
	new_row = request.dict()
	print(new_row)
	user_id = str(new_row["user_id"])
	os.makedirs(f"data", exist_ok=True)
	csv_path = f"data/{user_id}.csv"
	print(csv_path)
	result = add_transaction_and_enrich(new_row, csv_path)
	mse = train_models(path=csv_path) 
	return PredictionResponse(
		statusCode=result["statusCode"],
		error=result["error"],
		message=result["message"],
		data={"percent": mse}
	)


