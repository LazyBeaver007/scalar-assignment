import uuid
import random
from datetime import timedelta

def generate_subtasks(tasks, team_user_ids):
    subtasks = []

    for task in tasks:
        if random.random() > 0.25:
            continue

        for _ in range(random.randint(2, 5)):
            created_at = task["created_at"]
            completed = random.random() < 0.7
            completed_at = None

            if completed:
                completed_at = created_at + timedelta(days=random.randint(1, 10))

            subtasks.append({
                "subtask_id": str(uuid.uuid4()),
                "parent_task_id": task["task_id"],
                "name": f"Subtask for {task['name']}",
                "assignee_id": None if random.random() < 0.2 else random.choice(team_user_ids),
                "due_date": task["due_date"],
                "completed": completed,
                "completed_at": completed_at
            })

    return subtasks
