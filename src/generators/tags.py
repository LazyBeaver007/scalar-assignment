import uuid
import random

TAG_NAMES = ["bug", "urgent", "blocked", "follow-up"]

def generate_tags(org_id):
    return [{
        "tag_id": str(uuid.uuid4()),
        "organization_id": org_id,
        "name": name
    } for name in TAG_NAMES]


def generate_task_tags(tasks, tags):
    task_tags = []

    for task in tasks:
        if random.random() < 0.15:
            tag = random.choice(tags)
            task_tags.append({
                "task_id": task["task_id"],
                "tag_id": tag["tag_id"]
            })

    return task_tags
