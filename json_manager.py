import json

class JSONManager:
    def __init__(self, file_path="network_data.json"):
        self.file_path = file_path

    def load_data(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"users": [], "connections": []}

    def save_data(self, data):
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)