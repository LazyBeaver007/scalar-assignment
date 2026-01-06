import uuid
import random
from datetime import timedelta

COMMENTS = [
    "Looks good to me.",
    "Completed as discussed.",
    "Pushed changes, please review.",
    "Following up on this.",
    "Resolved in latest update."
]

def generate_comments(tasks, users):
    comments = []
    user_ids = [u["user_id"] for u in users]

    for task in tasks:
        if not task["completed"]:
            continue

        if random.random() > 0.6:
            continue

        for _ in range(random.randint(1, 3)):
            author = task.get("assignee_id") or random.choice(user_ids)
            comments.append({
                "comment_id": str(uuid.uuid4()),
                "task_id": task["task_id"],
                "user_id": author,
                "content": random.choice(COMMENTS),
                "created_at": task["completed_at"] - timedelta(days=random.randint(0, 3))
            })

    return comments
