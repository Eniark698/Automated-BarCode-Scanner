from time import sleep

def run_main_loop():
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




    print('Waiting...')
    sleep(60 * repeat_time)  # Sleep for 5 minutes


if __name__ == "__main__":
    while True:
        run_main_loop()
