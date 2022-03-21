from huey import crontab
from huey.contrib.djhuey import periodic_task, task, signal
from huey.contrib import djhuey as huey
from Backend.views import export_data, backup_database

# Run at local time is: hour=5, minute = 1
@periodic_task(crontab(hour=5, minute=1))
def schedule_export_data():
    export_data(None)
    

# Run at local time is: hour=20, minute = 1
@periodic_task(crontab(hour=21, minute=30))
def schedule_export_data1():
    export_data(None)


# Run at local time is: hour=11, minute = 5
@periodic_task(crontab(hour=11, minute=5))
def schedule_export_data2():
    export_data(None)


# Run at local time is: hour=20, minute = 1
@periodic_task(crontab(hour=16, minute=5))
def schedule_backupdb():
    backup_database()