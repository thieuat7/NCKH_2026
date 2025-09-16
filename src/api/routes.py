from fastapi import APIRouter, HTTPException
from src.inference.schema import PredictionRequest, PredictionResponse
from src.inference.predictor import  preprocess_input

router = APIRouter()

@router.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
	try:
		result = preprocess_input(request)
		return result
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))
