
# BarCode scanner

Program scan file for barcode, detect it, and filter that files
If you read more, program have in input file of any photos type, scan for barcode in, gain that info, if correct-- write to postgres database, and move to another folder; if barcode is not correct-- move to folder with incorrect codes; if it is not photos file-- move to folder with problem files



## Installation

Clone this repo to selected folder

```bash
  cd 'your folder'
  git clone https://github.com/Eniark698/scan_proj.git
```
Your must have installed python version 3

Install all necessary packages for python
```bash
    python.exe pip install -r requirements.txt
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


## Deployment

To start using move config.json to C:/scan_proj/




## Environment config

To run this project, you will need to set up path to each directories where files is stored, and set up amount of days, after which, outdated files will be deleted:
#### parametr | default value 

`days_to_remove` |`90` -- amount of date, after which photos will be deleted

`path to placement of scan's folder` | `C:/scan_proj/scan/` -- placement for files that used to be scanned

`path to placement of done's folder` | `C:/scan_proj/done/` --
placement for files that will be scanned and barcode is ok detected; info about this files will be writed to postgres database

`path to placement of not done's folder` | `C:/scan_proj/not done/` --
placement for files that will be scanned and barcode is not ok detected

`path to placement of problem files's folder`| `C:/scan_proj/problem/` --
placement for files that can not be scanned because it is not photos

`path to placement of log's folder`| `C:/scan_proj/logs/` --
placement for log with encounted error during program executing 