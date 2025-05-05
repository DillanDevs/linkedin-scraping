import os
import subprocess
import logging
from datetime import datetime, timedelta
from argparse import ArgumentParser
from apscheduler.schedulers.blocking import BlockingScheduler
from scraping.pipeline import run as run_scrape
from backend.config.config_db import settings

# Configure logger
default_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=default_fmt)
logger = logging.getLogger("automation")

# Directory to store backups and retention policy
BACKUP_DIR = os.getenv("BACKUP_DIR", "backups")
RETENTION_DAYS = int(os.getenv("RETENTION_DAYS", "7"))


def backup_db() -> None:
    """
    Perform a PostgreSQL database dump to a timestamped file in BACKUP_DIR.
    Parses the DATABASE_URL to extract connection parameters and invokes pg_dump.
    """
    os.makedirs(BACKUP_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(BACKUP_DIR, f"backup_{timestamp}.sql")

    # Parse the SQLAlchemy URL for host, port, user, password, and database
    from sqlalchemy.engine import make_url

    url = make_url(settings.DATABASE_URL)
    host = url.host or "127.0.0.1"
    port = url.port or 5432
    user = url.username
    password = url.password
    database = url.database

    # Build and run the pg_dump command
    cmd = (
        f"PGPASSWORD='{password}' pg_dump "
        f"-h {host} -p {port} -U {user} {database} > {output_file}"
    )
    try:
        subprocess.check_call(cmd, shell=True)
        logger.info(f"Backup successful: {output_file}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Backup failed: {e}")


def cleanup_old_backups() -> None:
    """
    Delete backup files in BACKUP_DIR older than RETENTION_DAYS.
    """
    now = datetime.now()
    for filename in os.listdir(BACKUP_DIR):
        file_path = os.path.join(BACKUP_DIR, filename)
        if not os.path.isfile(file_path):
            continue

        modified_time = datetime.fromtimestamp(os.path.getmtime(file_path))
        if now - modified_time > timedelta(days=RETENTION_DAYS):
            os.remove(file_path)
            logger.info(f"Removed old backup: {file_path}")


def incremental_load(csv_path: str = "dataset_linkedin.csv") -> None:
    """
    Run an incremental load of the CSV data into the database.
    """
    from scraping.to_db import load_csv_to_db

    try:
        load_csv_to_db(csv_path)
        logger.info(f"Incremental load completed from {csv_path}")
    except Exception as e:
        logger.error(f"Incremental load failed: {e}")


def schedule_tasks() -> None:
    """
    Schedule periodic tasks using APScheduler:
      - Daily scraping at 01:00
      - Daily backup at 02:00
      - Daily cleanup at 02:12
    """
    scheduler = BlockingScheduler()
    scheduler.add_job(run_scrape, "cron", hour=1, minute=0)
    scheduler.add_job(backup_db, "cron", hour=10, minute=54)
    scheduler.add_job(cleanup_old_backups, "cron", hour=10, minute=55)
    logger.info("Scheduler started: scrape@01:00, backup@10:54, cleanup@010:55")
    scheduler.start()


def main() -> None:
    """
    CLI entry point. Parses arguments and dispatches to the appropriate function:
      scrape   : Run scraping pipeline immediately
      backup   : Perform a full database backup now
      cleanup  : Remove old backup files
      schedule : Start the scheduler loop
    """
    parser = ArgumentParser(
        description="Automation CLI: scrape, backup, cleanup, schedule"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("scrape", help="Run scraping pipeline now")
    subparsers.add_parser("backup", help="Perform a full DB backup")
    subparsers.add_parser("cleanup", help="Cleanup old backups")
    subparsers.add_parser("schedule", help="Start the APScheduler loop")

    args = parser.parse_args()

    if args.command == "scrape":
        run_scrape()
    elif args.command == "backup":
        backup_db()
    elif args.command == "cleanup":
        cleanup_old_backups()
    elif args.command == "schedule":
        schedule_tasks()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()





