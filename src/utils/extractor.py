from pathlib import Path
import csv
import sys


def extract_startup_names(input_csv: Path, output_txt: Path, count: int = 100):
	names = []
	with input_csv.open(newline="", encoding="utf-8") as f:
		reader = csv.DictReader(f)
		for row in reader:
			name = (row.get('Startup Name') or row.get('StartupName') or '').strip()
			if name:
				names.append(name)
			if len(names) >= count:
				break

	output_txt.parent.mkdir(parents=True, exist_ok=True)
	with output_txt.open('w', encoding='utf-8') as out:
		for n in names:
			out.write(n + '\n')

	return names


def main(argv=None):
	argv = argv or sys.argv[1:]
	here = Path(__file__).resolve()
	input_csv = here.parent / 'shark_tank.csv'
	output_txt = here.parents[2] / 'src' / 'data' / 'saas_companies.txt'
	count = 100
	if argv:
		try:
			count = int(argv[0])
		except Exception:
			pass

	names = extract_startup_names(input_csv, output_txt, count)
	print(f"Wrote {len(names)} names to {output_txt}")


if __name__ == '__main__':
	main()

