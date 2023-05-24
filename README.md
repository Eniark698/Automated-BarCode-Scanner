![plot](./image.png)

# Automated BarCode Scanner

Program scan file for barcode, detect it, and filter that files
If you read more, program have in input file of any photos type, scan for barcode in, gain that info, if correct-- write to postgres database, and move to another folder; if barcode is not correct-- move to folder with incorrect codes; if it is not photos file-- move to folder with problem files
After v3.1, scanner can rescan problem folder, if filename begin with check_word


## Installation

Clone this repo to selected folder

```bash
  cd 'your folder'
  git clone https://github.com/Eniark698/scan_proj.git
```
Your must have installed python version 3

Install all necessary packages for python
```bash
    python.exe -m pip install -r requirements.txt
```

or, if you do not want to use .txt file, than
```bash
    pip install pyzbar
    pip install psutil
    pip install tendo
    pip install Pillow
    pip install psycopg2-binary
    pip install psycopg2
    pip install pywin32
```
and, if u are using *nix systems, than
```bash
    sudo apt-get install libzbar0 #for ubuntu
    brew install zbar #for os x
```

## Deployment

To start using move config.json to F:/proc/

!Do not forget to install postres on your pc, or connect to it using network




## Environment config

To run this project, you will need to set up path to each directories where files is stored, and set up amount of days, after which, outdated files will be deleted, delay to scan file after inserting, repeat time between two executions of scripts, check_word to extract from problem folder:
#### parametr | default value

`days_to_remove` |`90` -- amount of date, after which photos will be deleted

`path to placement of scan's folder` | `F:/proc/scan/` -- placement for files that used to be scanned

`path to placement of done folder for code128` | `F:/proc/done/` --
placement for CODE128 scanned files

`path to placement of done folder for ean13 or code39` | `F:/proc/not done/` --
placement for ean13 and code39 scanned files

`path to placement of problem files's folder`| `F:/scan_proj/problem/` --
placement for files that can not be scanned because it is not photos, or for files, then have errors

`path to placement of log's folder`| `F:/scan_proj/logs/` --
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
