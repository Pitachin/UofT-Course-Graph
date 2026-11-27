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

FIELDS = ['name', 'prereq', 'exclusion', 'corequisite', 'breadth']

def _load_json(file: str) -> list[dict]:
    """Load json file and return info as list of dicts"""
    with open(file, 'r', encoding='utf-8') as f:
        return json.load(f)


def _save_json(courses: list[dict], file: str) -> None:
    """Save cleaned course records to a JSON file."""
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(courses, f, indent=4, ensure_ascii=False)


def _validate_codes(courses: list[dict]) -> None:
    """Validate all course codes."""
    for course in courses:
        code = course['code'].strip().upper()

        if re.fullmatch(PATTERN, code) is None and code not in EXCEPTIONS:
            raise ValueError(f'Invalid course code: {code}')

        course['code'] = code

def _group_courses(courses: list[dict]) -> dict[str, list[dict]]:
    """Group course records by course code."""
    groups = {}

    for course in courses:
        code = course['code']

        if code not in groups:
            groups[code] = []

        groups[code].append(course)

    return groups

def _normalize_field(value: str | None) -> str | None:
    """Normalize a course information field."""
    if value is None:
        return None

    value = value.strip()

    for prefix in ['Prerequisite:', 'Exclusion:', 'Corequisite:']:
        if value.startswith(prefix):
            value = value.removeprefix(prefix).strip()
            break

    if value.lower() in ['', 'none', 'n/a']:
        return None

    return value

def _normalize_courses(courses: list[dict]) -> None:
    """Normalize optional fields in all course records."""
    for course in courses:
        for key in FIELDS:
            course[key] = _normalize_field(course[key])

def _detect_conflicts(groups: dict[str, list[dict]]) -> None:
    """Detect conflicting non-empty fields among duplicate courses."""
    conflicts = []

    for code, records in groups.items():
        if len(records) <= 1:
            continue

        for key in FIELDS:
            values = set()

            for record in records:
                if record[key] is not None:
                    values.add(record[key])

            if len(values) > 1:
                conflicts.append((code, key, values))

    for conflict in conflicts:
        print(conflict)

    if conflicts:
        raise ValueError(f'{len(conflicts)} unresolved conflicts found.')

    print('No conflicts detected.')


def _merge_courses(groups: dict[str, list[dict]]) -> list[dict]:
    """Merge duplicate course records without losing non-empty fields."""
    courses = []

    for code, records in groups.items():
        merged = {'code': code}

        for key in FIELDS:
            merged[key] = None

            for record in records:
                if record[key] is not None:
                    merged[key] = record[key]
                    break

        sources = []

        for record in records:
            url = record['source_url']

            if url not in sources:
                sources.append(url)

        merged['source_urls'] = sources

        courses.append(merged)

    return courses


def main() -> None:
    """Clean and deduplicate the raw course dataset."""
    courses = _load_json('data/uoft_raw.json')

    print(f'Total records: {len(courses)}')

    _validate_codes(courses)
    _normalize_courses(courses)

    groups = _group_courses(courses)

    _detect_conflicts(groups)

    cleaned = _merge_courses(groups)

    _save_json(cleaned, 'data/uoft_cleaned.json')

    print(f'Unique courses: {len(cleaned)}')
    print(f'Duplicate records removed: {len(courses) - len(cleaned)}')
    print('Data cleaning completed successfully.')


if __name__ == '__main__':
    main()