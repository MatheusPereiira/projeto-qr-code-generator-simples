import json
import os
from datetime import datetime

DB_PATH = "data/history.json"

class JSONDatabase:
    def __init__(self, path=DB_PATH):
        self.path = path
        os.makedirs("data", exist_ok=True)

        if not os.path.exists(self.path):
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump({"history": []}, f, indent=4)

    def load(self):
        with open(self.path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save(self, data):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def add_entry(self, text, qr_color, bg_color, filepath=None):
        db = self.load()
        db["history"].append({
            "id": len(db["history"]),
            "text": text,
            "qr_color": qr_color,
            "bg_color": bg_color,
            "filepath": filepath,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        self.save(db)

    def delete_entry(self, entry_id: int):
        db = self.load()
        db["history"] = [item for item in db["history"] if item["id"] != entry_id]
        self.save(db)
