import requests
from bs4 import BeautifulSoup, Tag
import json

URL = {
    'art&sci': 'https://artsci.calendar.utoronto.ca/search-courses',
    'utm': 'https://utm.calendar.utoronto.ca/course-search',
    'utsc': 'https://utsc.calendar.utoronto.ca/search-courses',
    'engineering': 'https://engineering.calendar.utoronto.ca/search-courses',
    "daniels": "https://daniels.calendar.utoronto.ca/search-courses",
    "kpe": "https://kpe.calendar.utoronto.ca/search-courses",
    "ischool": "https://ischool.calendar.utoronto.ca/search-courses",
    "music": "https://music.calendar.utoronto.ca/search-courses",
    "nursing": "https://nursing.calendar.utoronto.ca/search-courses",
    "pharmacy": "https://pharmacy.calendar.utoronto.ca/search-courses",
    "md": "https://md.calendar.utoronto.ca/search-courses",
    "sgs": "https://sgs.calendar.utoronto.ca/search-courses",
    "oise": "https://oise.academic-guide.utoronto.ca/search-courses",
    "law-jd": "https://jackmanlaw.utoronto.ca/jd-program/course-list",
    "law-first-year": "https://jackmanlaw.utoronto.ca/jd-program/first-year-course-assignments",
    "law-graduate": "https://jackmanlaw.utoronto.ca/graduate-programs/course-list",
    "dentistry": "https://www.dentistry.utoronto.ca/sites/default/files/2026-11/2026-2027%20FACULTY-CALENDAR.pdf",
}


def _extract_text(tag: Tag | None) -> str | None:
    """Return the text of tag. If it is None then return None."""
    return tag.get_text(" ", strip=True) if tag is not None else None


def _get_page(url: str) -> BeautifulSoup:
    """Retrieve the webpage at given <url> and return parsed HTML."""
    headers = {
        "User-Agent": "TrueBlue/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    r = requests.get(url, headers=headers, timeout=15)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def _get_last_page(soup: BeautifulSoup) -> int:
    """Return the zero-based index of the last page of the course catalogue.

    Return 0 if the catalogue contains only one page.
    """
    last_page = soup.select_one('a[title="Go to last page"]')

    if last_page is None:
        return 0

    href = last_page['href']
    return int(''.join(c for c in href if c.isdigit()))

def _parse_course(
        course: Tag,
        page: int,
        page_url: str
    ) -> dict[str, str | None]:
    """Extract course information from the given HTML tag.

    Return a dictionary containing the course code, name, prerequisites,
    exclusions, corequisites, breadth requirements, and source URL.

    Missing optional fields are represented by None.
    """

    title_tag = course.select_one(
                '.js-views-accordion-group-header > div'
            )

    assert title_tag is not None

    title = title_tag.get('aria-label')
    # utsg case
    if title is None or ' - ' not in title:
        title = _extract_text(title_tag)
    # utm case
    if title is not None:
        title = title.replace(' • ', ' - ', 1)

    print(repr(title))

    code, name = title.split(' - ', 1)

    prereq = _extract_text(
        course.select_one(
            '.views-field-field-prerequisite .field-content'
        )
    )

    exclusion = _extract_text(
        course.select_one(
            '.views-field-field-exclusion .field-content'
        )
    )

    corequisite = _extract_text(
        course.select_one(
            '.views-field-field-corequisite .field-content'
        )
    )

    breadth = _extract_text(
        course.select_one(
            '.views-field-field-breadth-requirements .field-content'
        ) 
    )

    return {
        'code': code,
        'name': name,
        'prereq': prereq,
        'exclusion': exclusion,
        'corequisite': corequisite,
        'breadth': breadth,
        'source_url': page_url
    }


def _save_json(all_courses: list[dict[str, str | None]], filename: str) -> None:
    """Save the collected course information to a JSON file.

    Overwrite the existing file if it already exists.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(all_courses, f, indent=4, ensure_ascii=False)


def scrape_courses(url: str) -> list[dict[str, str | None]]:
    """Scrape all the courses from the given course catalogue
    """
    all_courses = []
    info = _get_page(url)
    pages = _get_last_page(info)
    for page in range(pages + 1):
        print(f'Scraping page {page + 1}/{pages + 1}')
        curr_url = url + f'?page={page}'
        curr_info = _get_page(curr_url)

        courses = curr_info.select('.view-content > .views-row')
        for course in courses:
            course_info = _parse_course(course, page, curr_url)
            all_courses.append(course_info)

    return all_courses

if __name__ == '__main__':

    for faculty, url in URL.items():
        print(f'Scraping {faculty}...')

        all_courses = scrape_courses(url)
        _save_json(all_courses, f'{faculty}.json')

        print(f'Successfully scraped {len(all_courses)} courses.')