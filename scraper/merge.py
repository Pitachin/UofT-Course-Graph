import json
from pathlib import Path

all_courses = []

for file in Path('data/raw').glob('*_raw.json'):

    with open(file, 'r', encoding='utf-8') as f:
        courses = json.load(f)

    all_courses.extend(courses)

    print(f'{file.name}: {len(courses)} courses')


with open('data/uoft_raw.json', 'w', encoding='utf-8') as f:
    json.dump(all_courses, f, indent=4, ensure_ascii=False)

print(f'Total: {len(all_courses)} courses')