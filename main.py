from time import sleep

while True:
    # Call your other Python scripts here
    from input_values import importv
    from scanner import scan
    from remover import remove
    days, scanfolder, donefolder,oldfolder,problemfolder,logsfolder=importv()
    scan(scanfolder, donefolder,oldfolder,problemfolder,logsfolder)
    
    #remove(days, scanfolder, donefolder,oldfolder,problemfolder,logsfolder)
    

    

    # Sleep for a while before running the scripts again
    sleep(5*60)  # Sleep for 5 minutes