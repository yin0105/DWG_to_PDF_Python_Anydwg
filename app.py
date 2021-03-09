import os, shutil
from datetime import datetime
import subprocess
import threading


def PDF_Converter():
    #Please Update These Variables to Match your System Requirements
    pdf_folder = r"e:\pdfout"
    work_folder = r"e:\temp\dwg_converter"
    search_folders = [r"E:\Vaults\files\Drawings"]
    archive_folder = r"E:\Vaults\files\Drawings_Archive"
    dp_executable_path = r"C:\Program Files (x86)\Any DWG to PDF Converter Pro\dp.exe"
    dp_option_PDFColor = r"BlackWhite"      #Valid Options are TrueColors, GrayScale, BlackWhite
    dp_option_PDFQuality = r"High"          #Valid Options are Normal, Medium, High, Highest
    dp_option_HIDE = r"true"                #Valid Options are true or false
    dp_option_RUNMANY = r"false"            #Valid Options are true or fales --- this is setup so that your PDF Generator will run ALL files at once or one at a time
    rerun_wait_time = 5            #Time to wait in seconds before re_running_script --- change the number inside float() --- IF SET TO 0... this script only runs once
    
    if os.path.isdir(work_folder):
        shutil.rmtree(work_folder)
    os.mkdir(work_folder)
    
    for search_folder in search_folders:
        for root, dirs, files in os.walk(search_folder): 
            for file in files:     
                if file[-3:].lower() == "dwg":                 
                    try:
                        source_file = root + "\\" + file
                        shutil.copyfile(source_file, os.path.join(work_folder, file))
                        print("i'll print this file", work_folder + '\\' + file, "to this location as a PDF", pdf_folder + '\\' + file)
                        if dp_option_RUNMANY == 'false':
                            file_convert_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            print(file_convert_time)
                            subprocess.call([dp_executable_path, '/InFile', work_folder + '\\' + file, '/OutFile', pdf_folder + '\\' + file, '/ConvertType', 'DWG2PDF', '/PDFColor', dp_option_PDFColor, '/PDFQuality', dp_option_PDFQuality,'/RECOVER', '/HIDE'])
                            shutil.move(source_file, os.path.join(archive_folder, file))
                        else:
                            print("Window Shown")

                    except OSError:                    
                        mtime = 0
    if dp_option_RUNMANY == 'true':
        subprocess.call([dp_executable_path, '/InFolder', work_folder, '/OutFolder', pdf_folder, '/ConvertType', 'DWG2PDF', '/PDFColor', dp_option_PDFColor, '/PDFQuality', dp_option_PDFQuality, '/RECOVER' ])
    #else:
    #   print("why are you not doing everything at once")
      
    shutil.rmtree(work_folder)
    print("waiting for start PDF_Converter() again.")
    threading.Timer(rerun_wait_time * 60, PDF_Converter).start()

PDF_Converter()
