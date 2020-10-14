pdf_folder = r"E:\Workspace\Python Projects\DWG_to_PDF_python\pdf"
work_folder = r"D:\temp"
search_folders = [r"E:\Workspace\Python Projects\DWG_to_PDF_python\dwg\74"]
dp_executable_path = r"D:\Program Files (x86)\Any DWG to PDF Converter Pro\dp.exe"


from os.path import join, dirname
from dotenv import load_dotenv
import os, dotenv, shutil
from datetime import datetime
import subprocess

start_time = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

last_date = os.environ.get('LAST_DATE')
if os.path.isdir(work_folder):
    shutil.rmtree(work_folder)
os.mkdir(work_folder)

for search_folder in search_folders:
    for root, dirs, files in os.walk(search_folder): 
        for file in files:     
            if file[-3:].lower() == "dwg":                 
                try:
                    source_file = root + "\\" + file
                    mtime = os.path.getctime(source_file)
                    created_date = datetime.fromtimestamp(mtime)
                    if created_date > datetime.strptime(last_date, '%Y-%m-%d %H:%M:%S'):
                        shutil.copyfile(source_file, os.path.join(work_folder, file))
                        
                except OSError:                    
                    mtime = 0
for root, dirs, files in os.walk(work_folder): 
    for file in files:
        subprocess.call([dp_executable_path, '/InFile', root + "\\" + file, '/OutFile', pdf_folder + '\\' + file[:-3] + 'pdf'])
shutil.rmtree(work_folder)


dotenv.set_key(dotenv_path, "LAST_DATE", start_time)