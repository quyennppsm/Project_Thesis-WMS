from wms.celery import app
import subprocess

def run_layout_exe():
    exe_path = 'C:/Users/magnu/OneDrive/Documents/GitHub/Project_Thesis-WMS/software/inventory/wms/middleware/build/layout.exe'
    cmd = [exe_path]
    subprocess.run(cmd)

@app.task
def task_celery():      
    print(f" celery is online")
    return "....."


@app.task
def task_csv_layout():
    print(f" summoning layout.exe")
    run_layout_exe()
    return "[layout.exe]"

from celery import shared_task

@shared_task
def run_import_task():
    print(f" summoning import.py")
    subprocess.run(['python', 'controller/import.py'])
    return "[import.py]"