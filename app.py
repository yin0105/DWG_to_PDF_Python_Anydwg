import os, shutil
from datetime import datetime
import subprocess
import threading, json
from os import path

pdf_folder = r"e:\pdfout"
work_folder = r"e:\temp\dwg_converter"
search_folders = [r"E:\Vaults\files\Drawings"]
dp_executable_path = r"C:\Program Files (x86)\Any DWG to PDF Converter Pro\dp.exe"
dp_option_PDFColor = r"BlackWhite"      #Valid Options are TrueColors, GrayScale, BlackWhite
dp_option_PDFQuality = r"High"          #Valid Options are Normal, Medium, High, Highest
dp_option_HIDE = r"true"                #Valid Options are true or false
dp_option_RUNMANY = r"false"            #Valid Options are true or fales --- this is setup so that your PDF Generator will run ALL files at once or one at a time
rerun_wait_time = 5            #Time to wait in minute before re_running_script --- change the number inside float() --- IF SET TO 0... this script only runs once
pdf_json = {}


def get_last_timestamp(ff):
    mtime = os.path.getmtime(ff)
    if mtime < os.path.getctime(ff) : mtime = os.path.getctime(ff)
    return datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')


def initial_seed():
    global pdf_folder, pdf_json
    
    for file in os.listdir(pdf_folder):    
        if file[-3:].lower() == "pdf":                 
            file_name = file[:-4]
            pdf_json[file_name] = get_last_timestamp(pdf_folder + "\\" + file)
    fJSON = open('pdf_list.json', 'w')
    fJSON.write(json.dumps(pdf_json, sort_keys=True,
                           indent=2, separators=(',', ': ')))
    fJSON.close()


def read_json():
    global pdf_json
    with open('pdf_list.json') as json_file:
        pdf_json = json.load(json_file)
    print(pdf_json)


def PDF_Converter():
    if not path.exists("pdf_list.json"):
        initial_seed()
    else:
        read_json()

    if os.path.isdir(work_folder):
        shutil.rmtree(work_folder)
    os.mkdir(work_folder)
    
    for search_folder in search_folders:
        for root, dirs, files in os.walk(search_folder): 
            for file in files:     
                if file[-3:].lower() == "dwg":                 
                    try:
                        source_file = root + "\\" + file
                        source_file_timestamp = get_last_timestamp(source_file)
                        if source_file in pdf_json.keys:
                            if source_file_timestamp <= pdf_json[source_file]: 
                                continue
                        
                        pdf_json[source_file] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        shutil.copyfile(source_file, os.path.join(work_folder, file))
                        print("i'll print this file", work_folder + '\\' + file, "to this location as a PDF", pdf_folder + '\\' + file)
                        if dp_option_RUNMANY == 'false':
                            file_convert_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            print(file_convert_time)
                            subprocess.call([dp_executable_path, '/InFile', work_folder + '\\' + file, '/OutFile', pdf_folder + '\\' + file, '/ConvertType', 'DWG2PDF', '/PDFColor', dp_option_PDFColor, '/PDFQuality', dp_option_PDFQuality,'/RECOVER', '/HIDE'])
                        else:
                            print("Window Shown")
    
                    except OSError:                    
                        mtime = 0
    if dp_option_RUNMANY == 'true':
        subprocess.call([dp_executable_path, '/InFolder', work_folder, '/OutFolder', pdf_folder, '/ConvertType', 'DWG2PDF', '/PDFColor', dp_option_PDFColor, '/PDFQuality', dp_option_PDFQuality, '/RECOVER' ])
      
    shutil.rmtree(work_folder)

    fJSON = open('pdf_list.json', 'w')
    fJSON.write(json.dumps(pdf_json, sort_keys=True,
                           indent=2, separators=(',', ': ')))
    fJSON.close()

    threading.Timer(rerun_wait_time * 60, PDF_Converter).start()

PDF_Converter()