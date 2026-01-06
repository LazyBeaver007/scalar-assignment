import uuid
import random
def generate_custom_fields(projects):
    fields = []

    for project in projects:
        fields.append({
            "field_id": str(uuid.uuid4()),
            "project_id": project["project_id"],
            "name": "Priority",
            "field_type": "enum"
        })
        fields.append({
            "field_id": str(uuid.uuid4()),
            "project_id": project["project_id"],
            "name": "Effort",
            "field_type": "number"
        })

    return fields

PRIORITIES = ["Low", "Medium", "High"]

def generate_custom_field_values(tasks, field_defs):
    values = []

    for task in tasks:
        for field in field_defs:
            if field["project_id"] != task["project_id"]:
                continue

            if field["name"] == "Priority":
                value = random.choice(PRIORITIES)
            elif field["name"] == "Effort":
                value = str(random.randint(1, 8))
            else:
                value = None

            values.append({
                "task_id": task["task_id"],
                "field_id": field["field_id"],
                "value": value
            })

    return values
