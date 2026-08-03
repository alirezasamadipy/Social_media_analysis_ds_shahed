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

    def add_user(self, user_name):
        data = self.load_data()
        user_name = user_name.strip()
        if user_name and user_name not in data["users"]:
            data["users"].append(user_name)
            self.save_data(data)
            return True
        return False

    def remove_user(self, user_name):
        data = self.load_data()
        user_name = user_name.strip()
        if user_name in data["users"]:
            data["users"].remove(user_name)
            data["connections"] = [c for c in data["connections"] if user_name not in c]
            self.save_data(data)
            return True
        return False

    def add_connection(self, u1, u2):
        data = self.load_data()
        u1, u2 = u1.strip(), u2.strip()
        
        
        if not u1 or not u2 or u1 == u2:
            return False
        
        
        if u1 not in data["users"] or u2 not in data["users"]:
            return False
        
        
        if [u1, u2] not in data["connections"] and [u2, u1] not in data["connections"]:
            data["connections"].append([u1, u2])
            self.save_data(data)
            return True
            
        return False

    def remove_connection(self, u1, u2):
        data = self.load_data()
        u1, u2 = u1.strip(), u2.strip()
        initial_len = len(data["connections"])
        data["connections"] = [c for c in data["connections"] if not (u1 in c and u2 in c)]
        if len(data["connections"]) < initial_len:
            self.save_data(data)
            return True
        return False
