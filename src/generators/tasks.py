import uuid
import random
from datetime import timedelta
from pathlib import Path

from utils.llm import generate_batch



PROMPT_DIR = Path(__file__).resolve().parent.parent / "prompts"

TASK_NAME_CACHE = {}
TASK_DESC_CACHE = {}

FALLBACK_TASK_NAMES = {
    "engineering": [
        "Update API contract",
        "Fix authentication issue",
        "Refactor data pipeline",
        "Add logging support",
        "Optimize query performance"
    ],
    "marketing": [
        "Prepare campaign brief",
        "Review landing page copy",
        "Finalize content calendar"
    ],
    "operations": [
        "Update onboarding checklist",
        "Review vendor agreement",
        "Audit access permissions"
    ]
}

FALLBACK_TASK_DESCRIPTIONS = {
    "engineering": [
        "Refactor existing implementation to improve maintainability.",
        "Investigate reported issue and document findings.",
        "Apply fixes and validate behavior with tests."
    ],
    "marketing": [
        "Coordinate with stakeholders to finalize campaign details.",
        "Review copy and ensure alignment with messaging guidelines."
    ],
    "operations": [
        "Review current process and identify gaps.",
        "Update documentation and notify relevant teams."
    ]
}


def load_prompt(filename: str) -> str:
    return (PROMPT_DIR / filename).read_text()

def get_task_names(project_type):
    if project_type not in TASK_NAME_CACHE:
        prompt = load_prompt("task_names.txt").format(
            project_type=project_type
        )
        names = generate_batch(prompt, n=50)

        if not names:
            names = FALLBACK_TASK_NAMES[project_type]

        TASK_NAME_CACHE[project_type] = names

    return TASK_NAME_CACHE[project_type]

def get_task_descriptions(project_type):
    if project_type not in TASK_DESC_CACHE:
        prompt = load_prompt("task_descriptions.txt").format(
            project_type=project_type
        )
        descs = generate_batch(prompt, n=50)

        if not descs:
            descs = FALLBACK_TASK_DESCRIPTIONS[project_type]

        TASK_DESC_CACHE[project_type] = descs

    return TASK_DESC_CACHE[project_type]


def generate_tasks(project, section_ids, team_user_ids, start_date):
    tasks = []
    n_tasks = random.randint(40, 70)

    completion_rate = {
        "engineering": 0.8,
        "marketing": 0.55,
        "operations": 0.65
    }[project["project_type"]]

    task_names = get_task_names(project["project_type"])
    task_descs = get_task_descriptions(project["project_type"])

    for _ in range(n_tasks):
        task_id = str(uuid.uuid4())
        created_at = start_date + timedelta(days=random.randint(0, 180))

        assignee = None if random.random() < 0.15 else random.choice(team_user_ids)

        # Due date logic
        due_date = None
        if random.random() > 0.10:
            delta = random.choice([7, 14, 30, 60, 90])
            due_date = (created_at + timedelta(days=delta)).date()

        # Completion logic
        completed = random.random() < completion_rate
        completed_at = None
        if completed:
            completed_at = created_at + timedelta(days=random.randint(1, 14))

        # Description distribution
        description = None
        if random.random() > 0.20:
            description = random.choice(task_descs)

        tasks.append({
            "task_id": task_id,
            "project_id": project["project_id"],
            "section_id": random.choice(section_ids),
            "name": random.choice(task_names),
            "description": description,
            "assignee_id": assignee,
            "due_date": due_date,
            "created_at": created_at,
            "completed": completed,
            "completed_at": completed_at
        })

    return tasks
