# UofT-Course-Networks

### Intro

This is an independent research project exploring the structure of the University of Toronto's academic curriculum for the 2026–2027 academic year through graph theory & network science.

Inspired by Pavlos Stavrinides and Konstantin Zuev's work on Course-Prerequisite Networks (hereafter referred to as CPNs), this project aims to reproduce and extend the original research using course data scraped from UofT's academic calendars across all three campuses and various academic divisions.

### Process

1. Scrape all course information, including `code`, `name`, `prereq`, `exclusion`, `department_name`, `campus`, `source`, and `source_url`.

For instance, take our notorious pure math course, `MAT158H1`. The corresponding JSON looks like this:

```json
{
    "code": "MAT158H1",
    "name": "Analysis 1A",
    "prereq": "High school calculus",
    "exclusion": "MAT157Y1 / MAT157Y5 / MAT157H5",
    "department_name": "Department of Mathematics",
    "campus": "St. George",
    "source": "artsci",
    "source_url": "https://artsci.calendar.utoronto.ca/search-courses?page=103"
}
```

2. Model and visualize CPNs using [Gephi](https://gephi.org/) and conduct statistical analysis.
3. Write something interesting.

### Data Sources

- [UofT Academic Calendars](https://calendar.utoronto.ca/)
- [Faculty of Arts & Science](https://artsci.calendar.utoronto.ca/search-courses)
- [University of Toronto Mississauga (UTM)](https://utm.calendar.utoronto.ca/course-search)
- [University of Toronto Scarborough (UTSC)](https://utsc.calendar.utoronto.ca/search-courses)
- [Faculty of Applied Science & Engineering](https://engineering.calendar.utoronto.ca/search-courses)
- [John H. Daniels Faculty of Architecture, Landscape, and Design](https://daniels.calendar.utoronto.ca/search-courses)
- [Faculty of Kinesiology & Physical Education](https://kpe.calendar.utoronto.ca/search-courses)
- [Faculty of Information (iSchool)](https://ischool.calendar.utoronto.ca/search-courses)
- [Faculty of Music](https://music.calendar.utoronto.ca/search-courses)
- [Lawrence Bloomberg Faculty of Nursing](https://nursing.calendar.utoronto.ca/search-courses)
- [Leslie Dan Faculty of Pharmacy](https://pharmacy.calendar.utoronto.ca/search-courses)
- [School of Graduate Studies (SGS)](https://sgs.calendar.utoronto.ca/search-courses)
- [Ontario Institute for Studies in Education (OISE)](https://oise.academic-guide.utoronto.ca/search-courses)


### Finding

###### 1.1 Code Pattern

1. UTSG course
e.g. `MAT158H1` -> `[A-Z]{3}\d{3}[HY][10]` ( Exception: `APS299Y0` at Engineering )
2. UTM course
e.g. `MAT137H5` -> `[A-Z]{3}\d{3}[HY]5`
3. UTSC course
e.g. `MATA31H3` -> `[A-Z]{4}\d{2}[HY]3`
4. SGS
e.g. `STA4518H` -> `[A-Z]{3}\d{4}[HY]`

Thus, in general, the regular expression of all course code should be:
```
pattern = {
    r'\b(?:[A-Z]{3}\d{3}[HY][015]|[A-Z]{4}\d{2}[HY]3|[A-Z]{3}\d{4}[HY])\b'
}
```


### Reference

1. [Course-Prerequisite Networks for Analyzing and Understanding Academic Curricula](https://arxiv.org/abs/2210.01269)