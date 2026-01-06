
from pathlib import Path
import sqlite3

DB_PATH = Path("output") / "asana_simulation.sqlite"


def show_first_rows(conn, table, limit=5):
	cur = conn.cursor()
	try:
		cur.execute(f"SELECT * FROM {table} LIMIT ?", (limit,))
	except Exception as e:
		print(f"Skipping {table}: {e}")
		return
	rows = cur.fetchall()
	if not rows:
		print(f"{table}: (no rows)")
		return
	cols = [d[0] for d in cur.description]
	print(f"\n{table} (showing up to {limit}) ")
	print(" | ".join(cols))
	for r in rows:
		print(" | ".join(str(x) for x in r))


def main():
	if not DB_PATH.exists():
		print(f"Database not found at {DB_PATH}. Run `src/main.py` first to generate it.")
		return

	conn = sqlite3.connect(DB_PATH)

	tables = [
		"organizations",
		"users",
		"teams",
		"team_memberships",
		"projects",
		"sections",
		"tasks",
		"subtasks",
		"comments",
		"custom_field_definitions",
		"custom_field_values",
		"tags",
		"task_tags",
	]

	for t in tables:
		show_first_rows(conn, t, limit=5)

	conn.close()


if __name__ == "__main__":
	main()

