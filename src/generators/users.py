import uuid
import random
from datetime import timedelta
from utils.data_loader import load_list, random_name

FIRST_NAMES = load_list("first_names.txt")
LAST_NAMES = load_list("last_names.txt")

def generate_users(org_id, n_users, start_date):
    users = []

    for i in range(n_users):
        user_id = str(uuid.uuid4())
        created_at = start_date + timedelta(days=random.randint(0, 540))

        
        if i < n_users * 0.05:
            role = "admin"
        else:
            role = "member"

        full_name = random_name(FIRST_NAMES, LAST_NAMES)
        email = full_name.lower().replace(" ", ".") + "@acme.com"

        users.append({
            "user_id": user_id,
            "organization_id": org_id,
            "full_name": full_name,
            "email": email,
            "role": role,
            "created_at": created_at
        })

    return users
