from time import sleep

while True:
    from input_values import importv
    from scanner import scan
    from remover import remove
    from rescanner import rescan
    #import all important path variables
    days, scanfolder, donefolder, oldfolder, problemfolder, logsfolder=importv()

    scan(scanfolder, donefolder,oldfolder,problemfolder,logsfolder)
    rescan(donefolder,problemfolder,logsfolder)
    remove(days,donefolder,logsfolder)
    

    

    # Sleep for a while before running the scripts again
    sleep(5 * 60)  # Sleep for 5 minutes