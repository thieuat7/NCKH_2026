import pandas as pd
import numpy as np
from tensorflow import keras
from src.training.data_processorV3 import DataProcessorV3
import joblib

def train_models(path=""):
    try:
        # 1️⃣ Đọc dữ liệu mới
        df_new = pd.read_csv(path, encoding="latin-1")
    except FileNotFoundError:
        raise FileNotFoundError(f"❌ File not found: {path}")
    except pd.errors.ParserError:
        raise ValueError(f"❌ Cannot parse CSV file: {path}")
    except Exception as e:
        raise RuntimeError(f"❌ Error reading data: {e}")

    try:
        # 2️⃣ Load preprocessor & transform dữ liệu mới
        processor = DataProcessorV3(model_dir="src/training/preprocessors")
        new_windows = processor.transform_new_data(df_new)

        # 3️⃣ Load model
        model = keras.models.load_model("models/autoencoderV3_model.keras") 

        # 4️⃣ Dự đoán và tính MSE
        reconstruction = model.predict(new_windows)
        mse = np.mean(np.power(new_windows - reconstruction, 2), axis=(1, 2))
        mse = mse[-1]

        # 5️⃣ Load threshold và tính % MSE
        threshold = joblib.load("models/lstm_threshold_V3.pkl")
        MSE = mse / threshold * 100

        return MSE

    except FileNotFoundError as e:
        raise FileNotFoundError(f"❌ Required file not found: {e}")
    except ValueError as e:
        raise ValueError(f"❌ Value error during processing: {e}")
    except Exception as e:
        raise RuntimeError(f"❌ Unexpected error during training/prediction: {e}")

# Example usage:
# if __name__ == "__main__":
#     path = "data/294828221.csv"
#     mse = train_models(path)
#     print("MSE %:", mse)
