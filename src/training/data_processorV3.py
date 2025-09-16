import pandas as pd
import numpy as np
import joblib
import os
from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder, MinMaxScaler

class DataProcessorV3:
    def __init__(self, seq_len=20, dayfirst=False, model_dir="preprocessors"):
        self.seq_len = seq_len
        self.dayfirst = dayfirst
        self.model_dir = model_dir

        self.user_encoder = None
        self.receiver_encoder = None
        self.scaler = None
        self.cat_encoder = None
        self.feature_means = {}  # lưu mean cho numeric features

        # numeric features (thêm cyclical encoding)
        self.numeric_features = [
            "transaction_amount",
            "account_balance_before_txn",
            "avg_sent_amount_prev",
            "avg_received_amount_prev",
            "deviation_from_avg_sent_amount",
            "deviation_from_avg_received_amount",
            "transaction_count_last_7d",
            "unix_time",
            "has_sent_before",
            "has_received_before",
            "hour_sin", "hour_cos",
            "dow_sin", "dow_cos"
        ]

        # categorical features
        self.categorical_features = [
            "transaction_type",
            "device_id"
        ]

    def _parse_timestamp(self, df):
        df = df.copy()
        df["timestamp"] = pd.to_datetime(
            df["timestamp"],
            dayfirst=self.dayfirst,
            errors="coerce"
        )
        if df["timestamp"].isna().any():
            median_time = df["timestamp"].dropna().median()
            df["timestamp"] = df["timestamp"].fillna(median_time)

        # unix time (trend dài hạn)
        df["unix_time"] = df["timestamp"].view("int64") // 10**9

        # time features
        df["time_of_day"] = df["timestamp"].dt.hour
        df["day_of_week"] = df["timestamp"].dt.dayofweek

        # cyclical encoding
        df["hour_sin"] = np.sin(2 * np.pi * df["time_of_day"] / 24)
        df["hour_cos"] = np.cos(2 * np.pi * df["time_of_day"] / 24)
        df["dow_sin"] = np.sin(2 * np.pi * df["day_of_week"] / 7)
        df["dow_cos"] = np.cos(2 * np.pi * df["day_of_week"] / 7)

        return df

    def fit_transform(self, csv_path, label_col=None):
        df = pd.read_csv(csv_path, encoding="latin-1")
        df = self._parse_timestamp(df)
        print("✅ Dataset shape:", df.shape)

        # split train/test theo thời gian
        df = df.sort_values("timestamp").reset_index(drop=True)
        split_idx = int(len(df) * 0.8)
        train_df = df.iloc[:split_idx].copy()
        test_df = df.iloc[split_idx:].copy()

        # Encode user_id
        self.user_encoder = OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1)
        train_df["user_id_encoded"] = self.user_encoder.fit_transform(train_df[["user_id"]]).astype(int)
        test_df["user_id_encoded"] = self.user_encoder.transform(test_df[["user_id"]]).astype(int)

        # Encode receiver_id
        self.receiver_encoder = OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1)
        train_df["receiver_id_encoded"] = self.receiver_encoder.fit_transform(train_df[["receiver_id"]]).astype(int)
        test_df["receiver_id_encoded"] = self.receiver_encoder.transform(test_df[["receiver_id"]]).astype(int)

        # Fill NaN numeric + scale (lưu mean)
        self.feature_means = {}
        for col in self.numeric_features:
            mean_val = train_df[col].mean()
            self.feature_means[col] = mean_val
            train_df[col] = train_df[col].fillna(mean_val)
            test_df[col] = test_df[col].fillna(mean_val)

        self.scaler = MinMaxScaler() 
        X_train_num = self.scaler.fit_transform(train_df[self.numeric_features])
        X_test_num = self.scaler.transform(test_df[self.numeric_features])

        # Encode categorical (one-hot)
        self.cat_encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
        X_train_cat = self.cat_encoder.fit_transform(train_df[self.categorical_features])
        X_test_cat = self.cat_encoder.transform(test_df[self.categorical_features])

        # Merge numeric + categorical
        X_train_all = np.concatenate([X_train_num, X_train_cat], axis=1)
        X_test_all = np.concatenate([X_test_num, X_test_cat], axis=1)

        # Create windows
        X_train = self.create_windows(train_df, X_train_all)
        X_test = self.create_windows(test_df, X_test_all)

        input_dim = X_train_all.shape[1]

        # Nếu supervised thì xử lý nhãn
        if label_col:
            y_train = train_df[label_col].values
            y_test = test_df[label_col].values
            y_train = self.create_windows(train_df, y_train.reshape(-1,1))
            y_test = self.create_windows(test_df, y_test.reshape(-1,1))

            print("✅ Data processing complete (supervised).")
            return X_train, X_test, y_train, y_test, input_dim
        else:
            print("✅ Data processing complete (unsupervised).")
            return X_train, X_test, input_dim

    def create_windows(self, df_subset, X_all_scaled):
        windows = []
        df_subset = df_subset.sort_values(["user_id_encoded", "timestamp"]).reset_index(drop=True)

        for _, group in df_subset.groupby("user_id_encoded"):
            idx = group.index.values
            user_features = X_all_scaled[idx]

            if len(user_features) < self.seq_len:
                pad_len = self.seq_len - len(user_features)
                padded = np.pad(user_features, ((pad_len, 0), (0, 0)), mode="constant")
                windows.append(padded)
            else:
                for i in range(len(user_features) - self.seq_len + 1):
                    windows.append(user_features[i:i+self.seq_len])

        return np.array(windows, dtype=np.float32)

    def transform_new_data(self, df_new, auto_load=True):
        if auto_load and (self.user_encoder is None or 
                      self.receiver_encoder is None or 
                      self.scaler is None or 
                      self.cat_encoder is None):
            self.load_processors()
        df_new = self._parse_timestamp(df_new)
        df_new["user_id_encoded"] = self.user_encoder.transform(df_new[["user_id"]]).astype(int)
        df_new["receiver_id_encoded"] = self.receiver_encoder.transform(df_new[["receiver_id"]]).astype(int)

        for col in self.numeric_features:
            df_new[col] = df_new[col].fillna(self.feature_means[col])

        X_num = self.scaler.transform(df_new[self.numeric_features])
        X_cat = self.cat_encoder.transform(df_new[self.categorical_features])
        X_all = np.concatenate([X_num, X_cat], axis=1)

        df_new = df_new.sort_values(["user_id_encoded", "timestamp"]).reset_index(drop=True)
        windows = self.create_windows(df_new, X_all)
        return windows

    # ---------------- SAVE / LOAD ----------------
    def save_processors(self):
        os.makedirs(self.model_dir, exist_ok=True)
        joblib.dump(self.user_encoder, os.path.join(self.model_dir, "user_encoder.pkl"))
        joblib.dump(self.receiver_encoder, os.path.join(self.model_dir, "receiver_encoder.pkl"))
        joblib.dump(self.scaler, os.path.join(self.model_dir, "scaler.pkl"))
        joblib.dump(self.cat_encoder, os.path.join(self.model_dir, "cat_encoder.pkl"))
        joblib.dump(self.feature_means, os.path.join(self.model_dir, "feature_means.pkl"))
        print("✅ Saved processors to", self.model_dir)

    def load_processors(self):
        self.user_encoder = joblib.load(os.path.join(self.model_dir, "user_encoder.pkl"))
        self.receiver_encoder = joblib.load(os.path.join(self.model_dir, "receiver_encoder.pkl"))
        self.scaler = joblib.load(os.path.join(self.model_dir, "scaler.pkl"))
        self.cat_encoder = joblib.load(os.path.join(self.model_dir, "cat_encoder.pkl"))
        self.feature_means = joblib.load(os.path.join(self.model_dir, "feature_means.pkl"))
        print("✅ Loaded processors from", self.model_dir)
