import time
from datetime import datetime, date
from bs4 import BeautifulSoup
import pandas as pd
from .utils import get_applicants_count
from .config import settings


def scrape_jobs(driver, keyword: str = "Python Developer") -> pd.DataFrame:

    search_url = (
        "https://www.linkedin.com/jobs/search/"
        f"?keywords={keyword.replace(' ', '%20')}"
    )
    driver.get(search_url)
    time.sleep(settings.SCRAPE_DELAY)

    for _ in range(settings.SCROLLS):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(settings.SCROLL_DELAY)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    cards = soup.select("div.base-search-card")
    jobs = []

    for card in cards:
        if len(jobs) >= settings.JOB_LIMIT:
            break

        link_el  = card.select_one("a.base-card__full-link")
        title_el = card.select_one("h3.base-search-card__title")
        date_el  = card.select_one("time")
        if not link_el or not title_el:
            continue

        raw_date = date_el["datetime"] if date_el and date_el.has_attr("datetime") else None
        days_since = None
        if raw_date:
            pub_date = datetime.fromisoformat(raw_date).date()
            days_since = (date.today() - pub_date).days

        title    = title_el.get_text(strip=True)
        company  = (card.select_one("h4.base-search-card__subtitle") or "").get_text(strip=True)
        location = (card.select_one("span.job-search-card__location") or "").get_text(strip=True)
        job_url  = link_el["href"].strip()

        applicants = get_applicants_count(driver, job_url)

        jobs.append({
            "title":             title,
            "company":           company,
            "location":          location,
            "date_posted":       raw_date,
            "days_since_posted": days_since,
            "job_url":           job_url,
            "applicants":        applicants
        })

    return pd.DataFrame(jobs)
