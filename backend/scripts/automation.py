import os
import subprocess
import logging
from datetime import datetime, timedelta
from argparse import ArgumentParser
from apscheduler.schedulers.blocking import BlockingScheduler
from scraping.pipeline import run as run_scrape
from backend.config.config_db import settings


default_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=default_fmt)
logger = logging.getLogger("automation")

BACKUP_DIR = os.getenv('BACKUP_DIR', 'backups')
RETENTION_DAYS = int(os.getenv('RETENTION_DAYS', '7'))


def backup_db():
    os.makedirs(BACKUP_DIR, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    outfile = os.path.join(BACKUP_DIR, f"backup_{ts}.sql")

    # Parsear la URL para conectar por TCP
    from sqlalchemy.engine import make_url
    url = make_url(settings.DATABASE_URL)
    host = url.host or "127.0.0.1"
    port = url.port or 5432
    user = url.username
    pwd  = url.password
    db   = url.database

    cmd = (
        f"PGPASSWORD='{pwd}' pg_dump -h {host} -p {port} -U {user} {db} > {outfile}"
    )
    try:
        subprocess.check_call(cmd, shell=True)
        logger.info(f"Backup successful: {outfile}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Backup failed: {e}")



def cleanup_old_backups():
    now = datetime.now()
    for fname in os.listdir(BACKUP_DIR):
        path = os.path.join(BACKUP_DIR, fname)
        if not os.path.isfile(path):
            continue
        mtime = datetime.fromtimestamp(os.path.getmtime(path))
        if now - mtime > timedelta(days=RETENTION_DAYS):
            os.remove(path)
            logger.info(f"Removed old backup: {path}")


def incremental_load(csv_path: str = "dataset_linkedin.csv"):
    from scraping.to_db import load_csv_to_db
    try:
        load_csv_to_db(csv_path)
        logger.info(f"Incremental load completed from {csv_path}")
    except Exception as e:
        logger.error(f"Incremental load failed: {e}")


def schedule_tasks():
    sched = BlockingScheduler()
    sched.add_job(run_scrape, 'cron', hour=1, minute=0, kwargs={})
    sched.add_job(backup_db, 'cron', hour=2, minute=0)
    sched.add_job(cleanup_old_backups, 'cron', hour=2, minute=12)
    logger.info("Scheduler started: daily scrape@1:00, backup@2:00, cleanup@3:00")
    sched.start()


def main():
    parser = ArgumentParser(description="Automation CLI: scrape, backup, cleanup, schedule")
    sub = parser.add_subparsers(dest='cmd', required=True)

    sub.add_parser('scrape', help='Run scraping pipeline now')
    sub.add_parser('backup', help='Perform a full DB backup')
    sub.add_parser('cleanup', help='Cleanup old backups')
    sub.add_parser('schedule', help='Start the APScheduler loop')

    args = parser.parse_args()

    if args.cmd == 'scrape':
        run_scrape()
    elif args.cmd == 'backup':
        backup_db()
    elif args.cmd == 'cleanup':
        cleanup_old_backups()
    elif args.cmd == 'schedule':
        schedule_tasks()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
