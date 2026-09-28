import json
from pathlib import Path

SAVE_FILE = Path(__file__).resolve().parents[2] / "data" / "save.json"

def save_tasks(data):
    with SAVE_FILE.open("w",encoding='utf-8') as file:
        json.dump(data, file, indent=4)
    
def load_tasks():
    if not SAVE_FILE.exists():
        return {
            "main":{}
        }
    if not SAVE_FILE.read_text():
        return {
            "main":{}
        }
    with SAVE_FILE.open("r",encoding='utf-8') as file:
        return json.load(file)
        