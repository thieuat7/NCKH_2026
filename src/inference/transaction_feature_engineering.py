import pandas as pd
import numpy as np
import os
from typing import Dict

def add_transaction_and_enrich(new_row: dict, csv_path: str) -> dict:
    try:
        # ==== 1. Tạo thư mục nếu chưa có ====
        os.makedirs(os.path.dirname(csv_path), exist_ok=True)

        # ==== 2. Đọc toàn bộ CSV nếu có ====
        if os.path.exists(csv_path) and os.stat(csv_path).st_size > 0:
            df = pd.read_csv(csv_path, parse_dates=["timestamp"], encoding="utf-8-sig")
            print(f"📂 Đọc CSV thành công: {len(df)} dòng")
        else:
            df = pd.DataFrame()
            print("📂 File CSV rỗng hoặc không tồn tại. Tạo mới.")

        # ==== 3. Thêm giao dịch mới ====
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

        # ==== 4. Chuẩn hóa dữ liệu ====
        df["transaction_amount"] = df["transaction_amount"].astype(float)
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce", utc=True).dt.tz_localize(None)

        df["transaction_type"] = df["transaction_type"].astype(str).str.strip().str.lower()
        df["transaction_type"] = df["transaction_type"].apply(
            lambda x: "receive" if "receiv" in x else "send"
        )

        # ==== 5. Sắp xếp theo thời gian ====
        df = df.sort_values("timestamp").reset_index(drop=True)

        # ==== 6. Tính toán các chỉ số ====
        is_receive = df["transaction_type"] == "receive"
        is_send = ~is_receive

        df["send_amount"] = df["transaction_amount"].where(is_send, 0.0)
        df["send_flag"] = is_send.astype(int)
        df["cum_send_sum"] = df["send_amount"].cumsum()
        df["cum_send_count"] = df["send_flag"].cumsum()
        df["avg_sent_amount_prev"] = (df["cum_send_sum"].shift(1) / df["cum_send_count"].shift(1)).fillna(0)

        df["recv_amount"] = df["transaction_amount"].where(is_receive, 0.0)
        df["recv_flag"] = is_receive.astype(int)
        df["cum_recv_sum"] = df["recv_amount"].cumsum()
        df["cum_recv_count"] = df["recv_flag"].cumsum()
        df["avg_received_amount_prev"] = (df["cum_recv_sum"].shift(1) / df["cum_recv_count"].shift(1)).fillna(0)

        df["deviation_from_avg_sent_amount"] = np.where(
            is_send, df["transaction_amount"] - df["avg_sent_amount_prev"], 0
        )
        df["deviation_from_avg_received_amount"] = np.where(
            is_receive, df["transaction_amount"] - df["avg_received_amount_prev"], 0
        )

        g = df.set_index("timestamp")
        df["transaction_count_last_7d"] = (
            g["transaction_id"].rolling("7d").count().shift(1).fillna(0).astype(int).reset_index(drop=True)
        )

        # has_sent_before / has_received_before
        df["has_sent_before"] = 0
        df["has_received_before"] = 0
        sent_pairs, recv_pairs = set(), set()
        for i, row in df.iterrows():
            u, r, t = row["user_id"], row["receiver_id"], row["transaction_type"]
            if (u, r) in sent_pairs:
                df.at[i, "has_sent_before"] = 1
            if (u, r) in recv_pairs:
                df.at[i, "has_received_before"] = 1
            if t == "send":
                sent_pairs.add((u, r))
            else:
                recv_pairs.add((u, r))

        # ==== 7. Xóa cột phụ trước khi lưu ====
        df = df.drop(columns=[
            "send_amount", "send_flag", "cum_send_sum", "cum_send_count",
            "recv_amount", "recv_flag", "cum_recv_sum", "cum_recv_count"
        ], errors="ignore")

        # ==== 8. Lưu lại toàn bộ CSV ====
        df.to_csv(csv_path, index=False, encoding="utf-8-sig")
        print(f"✅ Đã lưu {len(df)} giao dịch sau khi tính toán lại.")

        return {
            "statusCode": 200,
            "error": None,
            "message": "CALL API SUCCESS",
            "data": {"percent": len(df)}
        }

    except Exception as e:
        print(f"❌ Lỗi tổng thể trong hàm add_transaction_and_enrich: {e}")
        return {
            "statusCode": 500,
            "error": str(e),
            "message": "CALL API FAILED",
            "data": {"percent": 0}
        }
