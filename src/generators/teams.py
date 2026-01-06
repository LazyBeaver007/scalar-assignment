
import uuid
import random
from datetime import datetime, timedelta

def generate_teams(org_id):
    team_names = [
        "Platform Engineering", "Infra Engineering", "Mobile Engineering",
        "Growth Marketing", "Content Marketing",
        "Operations", "Finance", "IT Support"
    ]

    teams = []
    for name in team_names:
        teams.append({
            "team_id": str(uuid.uuid4()),
            "organization_id": org_id,
            "name": name,
            "created_at": datetime.now()
        })
    return teams

def generate_team_memberships(teams, users):
    memberships = []

    user_ids = [u["user_id"] for u in users]

    for team in teams:
        team_size = random.randint(8, 25)
        members = random.sample(user_ids, team_size)

        for uid in members:
            memberships.append({
                "team_id": team["team_id"],
                "user_id": uid,
                "joined_at": team["created_at"]
            })

    return memberships
