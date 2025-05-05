import time
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from selenium.common.exceptions import TimeoutException, WebDriverException
from .config import settings


def get_applicants_count(driver, job_url) -> int:
    last_exc = None
    for attempt in range(1, settings.APPLICANT_RETRIES + 1):
        try:
            driver.get(job_url)
            time.sleep(settings.APPLICANT_DELAY)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            el = soup.select_one("span.num-applicants__caption")
            if el:
                nums = re.findall(r"\d+", el.get_text())
                if nums:
                    return int(nums[-1])
            return None
        except (TimeoutException, WebDriverException) as e:
            last_exc = e
            time.sleep(settings.APPLICANT_DELAY)
    return None

def normalize_job_url(raw_url: str) -> str:
    parsed = urlparse(raw_url)
    path = parsed.path
    m = re.search(r"/jobs/view/(\d+)", path)
    if m:
        job_id = m.group(1)
        return f"https://www.linkedin.com/jobs/view/{job_id}"
    return f"{parsed.scheme}://{parsed.netloc}{path}"
