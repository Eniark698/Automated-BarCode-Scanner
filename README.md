![plot](./image.png)

# Automated BarCode Scanner

Program scan file for barcode, detect it, and filter that files
If you read more, program have in input file of any photos type, scan for barcode in, gain that info, if correct-- write to postgres database, and move to another folder; if barcode is not correct-- move to folder with incorrect codes; if it is not photos file-- move to folder with problem files
<br>After v3.1, scanner can rescan problem folder, if filename begin with check_word
<br>After v3.5, scanner use docker to containerization 

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
  docker compose up -d --build
```
<br>After v3.5 scanner use postgres from docker-compose



## Environment config

To run this project, you will need to set up path to each directories where files is stored, and set up amount of days, after which, outdated files will be deleted, delay to scan file after inserting, repeat time between two executions of scripts, check_word to extract from problem folder:
#### parametr | default value

`_comment_` | `/project/ is F:/proc/``  -- changes in directory name due to mounting it to docker container

`days_to_remove` |`90` -- amount of date, after which photos will be deleted

`path to placement of scan's folder` | `["/project/scan/","/project/scanMukachevo/","/project/scanSambir/", "/project/scanTernopil/", "/project/scanVinnytsia/", "/project/scanZhytomyr/", "/project/scanRivne/", "/project/scanLutsk/","/project/scanKhmelnytskyi/","/project/scanFrankivsk/","/project/scanChernivtsi/"]` -- placement for files that used to be scanned

`path to placement of done folder for code128` | `/project/done/` --
placement for CODE128 scanned files

`path to placement of done folder for ean13 or code39` | `/project/not done/` --
placement for ean13 and code39 scanned files

`path to placement of problem files's folder`| `["/project/problem/","/project/problemMukachevo/","/project/problemSambir/","/project/problemTernopil/","/project/problemVinnytsia/","/project/problemZhytomyr/","/project/problemRivne/","/project/problemLutsk/","/project/problemKhmelnytskyi/","/project/problemFrankivsk/","/project/problemChernivtsi/"]` --
placement for files that can not be scanned because it is not photos, or for files, then have errors

`path to placement of log's folder`| `/project/logs/` --
placement for log with encounted error during program executing

`delay to scan file`| `5` --
delay before scanning and moving file with good barcode

`repeat time between two executions of script`| `5` --
delay before executing script again

`check_word`| `IRIS` --
check word to gather file from problem folder and rescan it, using only filename


## Perfomance
The speed depends greatly on the processor power and the size of the photos



Depending on the power of your PC and the size of the photos, you can get a speed of up to `0.2 sec/file`
My PC server:
  -Intel Xeon E5-2650 v4 @2.2GHz
  -Files are on average 500kb in size, format JPEG



## Used By

This project is used by the following companies:

- BERTA group
![Logo](https://berta.ua/wp-content/uploads/2019/07/logo.svg)
