import os
import json

def load_json(file_path):
    """Load JSON data from a file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error: File {file_path} contains invalid JSON.")
        return []

def load_cosing_data(data_dir):
    """Load all COSING JSON files."""
    json_files = {
        "prohibited": load_json(os.path.join(data_dir, "prohibited_substances.json")),
        "restricted": load_json(os.path.join(data_dir, "restricted_substances.json")),
        "colorants": load_json(os.path.join(data_dir, "allowed_colorants.json")),
        "preservatives": load_json(os.path.join(data_dir, "allowed_preservatives.json")),
        "uv_filters": load_json(os.path.join(data_dir, "allowed_uv_filters.json"))
    }
    return json_files