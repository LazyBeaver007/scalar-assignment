from pathlib import Path
import random

BASE_PATH = Path(__file__).resolve().parent.parent / "data"

def load_list(filename):
    with open(BASE_PATH / filename, "r") as f:
        return [line.strip() for line in f if line.strip()]

def random_name(first_names, last_names):
    return f"{random.choice(first_names)} {random.choice(last_names)}"
