import json


def load_json(file_path):
    """
    Load JSON file data
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data

    except Exception as e:
        print(f"Error loading file: {e}")
        return []