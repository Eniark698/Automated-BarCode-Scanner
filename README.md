![plot](./image.png)

# Automated BarCode Scanner

Program scan file for barcode, detect it, and filter that files
If you read more, program have in input file of any photos type, scan for barcode in, gain that info, if correct-- write to postgres database, and move to another folder; if barcode is not correct-- move to folder with incorrect codes; if it is not photos file-- move to folder with problem files
<br>In this version, everything is working using windows services

## Installation

Clone this repo to selected folder

```bash
  cd 'your folder'
  git clone https://github.com/Eniark698/scan_proj.git
```
Your must have installed docker

All deps will be installed in auto mode

If you want not to use Docker, then 
```bash
    sudo apt-get install libzbar0 #for ubuntu
    brew install zbar #for os x
    #The zbar DLLs are included with the Windows Python wheels
```
If you see an ugly ImportError when importing pyzbar on Windows you will most likely need the Visual C++ Redistributable Packages for Visual Studio 2013. Install vcredist_x64.exe if using 64-bit Python, vcredist_x86.exe if using 32-bit Python.

## Deployment

To start using move config.json to F:/proc/

```bash
  cd Automated-BarCode-Scanner
  ./temp/scan_project.bat
  ./temp/dashboard_scan_project.bat
```

Make sure that you have installed psql


## Environment config

To run this project, you will need to set up path to each directories where files is stored, and set up amount of days, after which, outdated files will be deleted, delay to scan file after inserting, repeat time between two executions of scripts, check_word to extract from problem folder:
#### parameter | default value


`enable_multiprocessing` | `0` -- 1 for enable, 0 for disable (activate multiprocessing of scanfolder for scan each location in parallel(up to 11x faster))

`days_to_remove` |`90` -- amount of date, after which photos will be deleted

`path to placement of scan's folder` | `{"Lviv":"F:/proc/scan/"
        ,"Mukachevo":"F:/proc/scanMukachevo/"
        ,"Sambir":"F:/proc/scanSambir/"
        ,"Ternopil":"F:/proc/scanTernopil/"
        ,"Vinnytsia":"F:/proc/scanVinnytsia/"
        ,"Zhytomyr":"F:/proc/scanZhytomyr/"
        ,"Rivne":"F:/proc/scanRivne/"
        ,"Lutsk":"F:/proc/scanLutsk/"
        ,"Khmelnytskyi":"F:/proc/scanKhmelnytskyi/"
        ,"Frankivsk":"F:/proc/scanFrankivsk/"
        ,"Chernivtsi":"F:/proc/scanChernivtsi/"}` 
        
        -- placement for files that used to be scanned

`path to placement of done folder for code128` | `F:/proc/done/` --
placement for CODE128 scanned files

`path to placement of done folder for ean13 or code39` | `F:/proc/not done/` --
placement for ean13 and code39 scanned files

`path to placement of problem files's folder`| `{"Lviv":"F:/proc/problem/"
        ,"Mukachevo":"F:/proc/problemMukachevo/"
        ,"Sambir":"F:/proc/problemSambir/"
        ,"Ternopil":"F:/proc/problemTernopil/"
        ,"Vinnytsia":"F:/proc/problemVinnytsia/"
        ,"Zhytomyr":"F:/proc/problemZhytomyr/"
        ,"Rivne":"F:/proc/problemRivne/"
        ,"Lutsk":"F:/proc/problemLutsk/"
        ,"Khmelnytskyi":"F:/proc/problemKhmelnytskyi/"
        ,"Frankivsk":"F:/proc/problemFrankivsk/"
        ,"Chernivtsi":"F:/proc/problemChernivtsi/"}` 
        
        -- placement for files that can not be scanned because it is not photos, or for files, then have errors

`path to placement of log's folder`| `F:/proc/logs/` --
placement for log with encounted error during program executing

`delay to scan file`| `5` --
delay before scanning and moving file with good barcode

`repeat time between two executions of script`| `5` --
delay before executing script again

`check_word`| `IRIS` --
check word to gather file from problem folder and rescan it, using only filename


## Perfomance
The speed depends greatly on the processor power and the size of the photos
You can turn on multiprocessing to scan all teritorries in parallel


Depending on the power of your PC and the size of the photos, you can get a speed of up to `0.2 sec/file`
My PC server:
  -Intel Xeon E5-2650 v4 @2.2GHz
  -Files are on average 500kb in size, format JPEG



## Used By

This project is used by the following companies:

- BERTA group
![Logo](https://berta.ua/wp-content/uploads/2019/07/logo.svg)
