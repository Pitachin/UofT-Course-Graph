import json
from collections import Counter
import re

PATTERN = (
    r'\b(?:[A-Z]{3}\d{3}[HY][015]|[A-Z]{4}\d{2}[HY]3|[A-Z]{3}\d{4}[HY])\b'
           )

EXCEPTIONS = {
    'KPE433H',
    'ARC2016',
    'ARC3300',
    'RSM2026'
}

def _load_json(file: str) -> list[dict]:
    """Load json file and return info as list of dicts"""
    with open(file, 'r', encoding='utf-8') as f:
        return json.load(f)

def _detect_duplicate_course(courses: list[dict]) -> None:
    """Detect if there is a repeated data in JSON"""
    codes = [course['code'] for course in courses]
    count = Counter(codes)

    for code, freq in count.items():
        if freq > 1:
            print(f'{code}: {freq} occurrences!')

courses = _load_json('data/uoft_raw.json')
print(f'Total Courses: {len(courses)}')

#  _detect_duplicate_course(courses)

for course in courses:
    code = course['code'].strip().upper()
    if re.fullmatch(PATTERN, code) is None and code not in EXCEPTIONS:
        print(course)
