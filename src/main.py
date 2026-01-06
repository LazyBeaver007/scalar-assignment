import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

from generators.users import generate_users
from generators.teams import generate_teams, generate_team_memberships
from generators.projects import generate_projects, generate_sections
from generators.tasks import generate_tasks
from generators.subtasks import generate_subtasks
from generators.comments import generate_comments
from generators.custom_fields import generate_custom_fields, generate_custom_field_values
from generators.tags import generate_tags, generate_task_tags

DB_PATH = Path("output/asana_simulation.sqlite")
SCHEMA_PATH = Path("scheme.sql")

def load_schema(conn):
    with open(SCHEMA_PATH, "r") as f:
        conn.executescript(f.read())

def insert_many(conn, table, rows):
    if not rows:
        return
    cols = rows[0].keys()
    placeholders = ",".join(["?"] * len(cols))
    sql = f"INSERT INTO {table} ({','.join(cols)}) VALUES ({placeholders})"
    conn.executemany(sql, [tuple(r[c] for c in cols) for r in rows])

def main():
    DB_PATH.parent.mkdir(exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    load_schema(conn)

    now = datetime.now()
    org_id = "org-001"

   
    insert_many(conn, "organizations", [{
        "organization_id": org_id,
        "name": "Acme SaaS Inc.",
        "domain": "acme.com",
        "created_at": now - timedelta(days=540)
    }])

    
    users = generate_users(
        org_id=org_id,
        n_users=7000,
        start_date=now - timedelta(days=540)
    )
    insert_many(conn, "users", users)

   
    teams = generate_teams(org_id)
    insert_many(conn, "teams", teams)

    team_memberships = generate_team_memberships(teams, users)
    insert_many(conn, "team_memberships", team_memberships)

    
    projects = generate_projects(teams)
    insert_many(conn, "projects", projects)

    sections = generate_sections(projects)
    insert_many(conn, "sections", sections)

  
    all_tasks = []
    for project in projects:
        team_users = [
            m["user_id"] for m in team_memberships
            if m["team_id"] == project["team_id"]
        ]
        project_sections = [
            s["section_id"] for s in sections
            if s["project_id"] == project["project_id"]
        ]
        tasks = generate_tasks(
            project,
            project_sections,
            team_users,
            start_date=now - timedelta(days=180)
        )
        all_tasks.extend(tasks)

    insert_many(conn, "tasks", all_tasks)

   
    subtasks = generate_subtasks(all_tasks, [u["user_id"] for u in users])
    insert_many(conn, "subtasks", subtasks)


    comments = generate_comments(all_tasks, users)
    insert_many(conn, "comments", comments)

    
    field_defs = generate_custom_fields(projects)
    insert_many(conn, "custom_field_definitions", field_defs)

    field_values = generate_custom_field_values(all_tasks, field_defs)
    insert_many(conn, "custom_field_values", field_values)

   
    tags = generate_tags(org_id)
    insert_many(conn, "tags", tags)

    task_tags = generate_task_tags(all_tasks, tags)
    insert_many(conn, "task_tags", task_tags)

    conn.commit()
    conn.close()

    print("asana_simulation.sqlite generated ")

if __name__ == "__main__":
    main()
