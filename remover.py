def remove():
    from os import listdir
    from datetime import datetime
    from shutil import rmtree
    import json
    import exifread

    def days_between(d1, d2):
        d1 = datetime.strptime(d1, "%Y-%m-%d")
        d2 = datetime.strptime(d2, "%Y-%m-%d")
        return abs((d2 - d1).days)
    now_date=datetime.today().strftime('%Y-%m-%d')


    path='C:/scan_proj/'


    with open(path + 'config.json') as json_file:
            data = json.load(json_file)
            try:
                donefolder=data["path to placement of done`s folder"]
                logsfolder=data["path to placement of log`s folder"]
            except Exception as err:
                donefolder="C:/scan_proj/done/"
                logsfolder="C:/scan_proj/logs/"

                f=open(logsfolder + 'log_conf_rem.txt', 'a')
                f.write('--\n')
                f.write(str(Exception))
                f.write('\n')
                f.write(str(err))
                f.write('occurred on ' + str(datetime.now()))
                f.write('\n--\n\n\n')
                f.close()

    with open(path + 'config.json') as json_file:
        data = json.load(json_file)
        try:
            days=data["days_to_remove"]
        except Exception as err:
            days=100
            f=open(logsfolder + 'log_conf_rem.txt', 'a')
            f.write('--\n')
            f.write(str(Exception))
            f.write('\n')
            f.write(str(err))
            f.write('occurred on ' + str(datetime.now()))
            f.write('\n--\n\n\n')
            f.close()


    list=listdir(donefolder)
    for i in list:
        with open(donefolder + i, 'rb') as fh:
            tags = exifread.process_file(fh, stop_tag="EXIF DateTimeOriginal")
            dateTaken = tags["EXIF DateTimeOriginal"]
            dateTaken = dateTaken.strftime('%Y-%m-%d')
            if abs(days_between(now_date,dateTaken))>=days:
                rmtree(donefolder + str(i))

remove()
