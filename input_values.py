#import path`es and RemoveDays to working directories
def importv():
    import json    
    from datetime import datetime

    #make variables global to get it from another scripts
    #global  scanfolder, donefolder, oldfolder,problemfolder,logsfolder,delay,repeat_time,check_word

    #standart path to read config file
    path="F:/proc/"



    #open config file, read it, in case of error, import default values, write to log files
    with open(path + 'config.json') as json_file:
        data = json.load(json_file)
        
        try:
            days=data['days_to_remove']
            scanfolder=data["path to placement of scan`s folder"]
            donefolder=data["path to placement of done folder for code128"]
            oldfolder=data["path to placement of done folder for ean13 or code39"]
            problemfolder=data["path to placement of problem files`s folder"]
            logsfolder=data["path to placement of log`s folder"]
            delay=data["delay to scan file"]
            repeat_time=data["repeat time in minutes between two executions of script"]
            check_word=data["check_word"]
        except Exception as err:
            days=100
            scanfolder={"Lviv":"F:/proc/scan/"
                ,"Mukachevo":"F:/proc/scanMukachevo/"
                ,"Sambir":"F:/proc/scanSambir/"
                ,"Ternopil":"F:/proc/scanTernopil/"
                ,"Vinnytsia":"F:/proc/scanVinnytsia/"
                ,"Zhytomyr":"F:/proc/scanZhytomyr/"
                ,"Rivne":"F:/proc/scanRivne/"
                ,"Lutsk":"F:/proc/scanLutsk/"
                ,"Khmelnytskyi":"F:/proc/scanKhmelnytskyi/"
                ,"Frankivsk":"F:/proc/scanFrankivsk/"
                ,"Chernivtsi":"F:/proc/scanChernivtsi/"},
            
            donefolder="/project/done/"
            oldfolder="/project/not done/"
            problemfolder={"Lviv":"F:/proc/problem/"
                ,"Mukachevo":"F:/proc/problemMukachevo/"
                ,"Sambir":"F:/proc/problemSambir/"
                ,"Ternopil":"F:/proc/problemTernopil/"
                ,"Vinnytsia":"F:/proc/problemVinnytsia/"
                ,"Zhytomyr":"F:/proc/problemZhytomyr/"
                ,"Rivne":"F:/proc/problemRivne/"
                ,"Lutsk":"F:/proc/problemLutsk/"
                ,"Khmelnytskyi":"F:/proc/problemKhmelnytskyi/"
                ,"Frankivsk":"F:/proc/problemFrankivsk/"
                ,"Chernivtsi":"F:/proc/problemChernivtsi/"},
            
            logsfolder="/project/logs/"
            delay=5
            repeat_time=5
            check_word="IRIS"
            f=open(logsfolder + 'log_inp.txt', 'a')
            f.write('--\n')
            f.write(str(Exception))
            f.write('\n')
            f.write(str(err))
            f.write('occurred on ' + str(datetime.now()))
            f.write('\n--\n\n\n')
            f.close()
            return days, scanfolder, donefolder,oldfolder,problemfolder,logsfolder,delay,repeat_time,check_word


    
    #return imported values
    return days, scanfolder, donefolder,oldfolder,problemfolder,logsfolder,delay,repeat_time,check_word