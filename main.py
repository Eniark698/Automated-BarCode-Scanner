from time import sleep

while True:
    from input_values import importv
    from scanner import scan
    from remover import remove
    from rescanner import rescan
    from writing import write
    #import all important path variables
    pattern=r'[0-9]{5}\-[0-9]{7}_[0-9]{4}_[0-9]{1}_[a-zA-z]'
    days, scanfolder, donefolder, oldfolder, problemfolder, logsfolder, delay,repeat_time,check_word =importv()

    scan(scanfolder, donefolder,oldfolder,problemfolder,logsfolder,delay,pattern)
    rescan(donefolder,problemfolder,logsfolder,check_word,pattern)
    remove(days,donefolder,logsfolder)
    write(logsfolder)
    

    

    # Sleep for a while before running the scripts again
    sleep(5 * repeat_time)  # Sleep for 5 minutes