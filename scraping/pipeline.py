import logging
from .driver import init_driver, linkedin_login
from .scraper import scrape_jobs
from .to_db import load_csv_to_db
from .config import settings

logger = logging.getLogger(__name__)

def run(keyword: str = "Python Developer"):
    driver = init_driver(headless=True)
    try:
        linkedin_login(driver)
        df = scrape_jobs(driver, keyword)
        csv_path = "dataset_linkedin.csv"
        df.to_csv(csv_path, index=False)
        logger.info(f"CSV guardado en '{csv_path}' con {len(df)} registros.")
        load_csv_to_db(csv_path)
        logger.info("Datos volcados a la base de datos.")
    except Exception as e:
        logger.error(f"Error en pipeline: {e}", exc_info=True)
    finally:
        driver.quit()
        logger.info("Driver cerrado.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    run()