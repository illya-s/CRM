# from CRM.celery import app
from celery import shared_task
import subprocess, os
import datetime
from django.conf import settings

@shared_task
def backup_db():
    BACKUP_DIR = os.path.join(settings.BASE_DIR, "backups")
    os.makedirs(BACKUP_DIR, exist_ok=True)
    
    DATE_STR = datetime.datetime.now().strftime("%Y-%m-%d")
    BACKUP_FILE = os.path.join(BACKUP_DIR, f"backup_{DATE_STR}.sql")

    DB_NAME = settings.DATABASES["default"]["NAME"]
    DB_USER = settings.DATABASES["default"]["USER"]
    DB_PASSWORD = settings.DATABASES["default"].get("PASSWORD", "")

    DUMP_COMMAND = f"PGPASSWORD={DB_PASSWORD} pg_dump -U {DB_USER} -h localhost {DB_NAME} > {BACKUP_FILE}"
    subprocess.run(DUMP_COMMAND, shell=True)

    THIRTY_DAYS_AGO = datetime.datetime.now() - datetime.timedelta(days=30)
    for file in os.listdir(BACKUP_DIR):
        file_path = os.path.join(BACKUP_DIR, file)
        if os.path.isfile(file_path):
            file_date = datetime.datetime.fromtimestamp(os.path.getctime(file_path))
            if file_date < THIRTY_DAYS_AGO:
                os.remove(file_path)