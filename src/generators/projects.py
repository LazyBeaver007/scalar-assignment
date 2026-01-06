import uuid
import random
from datetime import datetime

PROJECT_TYPES = ["engineering", "marketing", "operations"]

def generate_projects(teams):
    projects = []

    for team in teams:
        for _ in range(random.randint(5, 12)):
            projects.append({
                "project_id": str(uuid.uuid4()),
                "team_id": team["team_id"],
                "name": f"{team['name']} Initiative",
                "project_type": random.choice(PROJECT_TYPES),
                "created_at": team["created_at"],
                "archived": 1 if random.random() < 0.2 else 0
            })

    return projects


def generate_sections(projects):
    sections = []
    default_sections = ["To Do", "In Progress", "Done"]

    for project in projects:
        for i, name in enumerate(default_sections):
            sections.append({
                "section_id": str(uuid.uuid4()),
                "project_id": project["project_id"],
                "name": name,
                "position": i
            })

    return sections
