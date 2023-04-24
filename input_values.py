#import path`es and RemoveDays to working directories
def importv():
    import json    
    from datetime import datetime

    #make variables global to get it from another scripts
    global  scanfolder, donefolder, oldfolder,problemfolder,logsfolder

    #standart path to read config file
    path="D:/proc/"



    #open config file, read it, in case of error, import default values, write to log files
    with open(path + 'config.json') as json_file:
        data = json.load(json_file)
        
        try:
            #path=data['path']
            days=data['days_to_remove']
            scanfolder=data["path to placement of scan`s folder"]
            donefolder=data["path to placement of done folder for code128"]
            oldfolder=data["path to placement of done folder for ean13 or code39"]
            problemfolder=data["path to placement of problem files`s folder"]
            logsfolder=data["path to placement of log`s folder"]
        except Exception as err:
            days=100
            #path="D:/proc/"
            scanfolder="D:/proc/scan/"
            donefolder="D:/proc/Processed/done/"
            oldfolder="D:/proc/Processed/not done/"
            problemfolder="D:/proc/Processed/problem/"
            logsfolder="D:/proc/logs/"

            f=open(logsfolder + 'log_inp.txt', 'a')
            f.write('--\n')
            f.write(str(Exception))
            f.write('\n')
            f.write(str(err))
            f.write('occurred on ' + str(datetime.now()))
            f.write('\n--\n\n\n')
            f.close()


    
    #return imported values
    return days, scanfolder, donefolder,oldfolder,problemfolder,logsfolder