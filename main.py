def run_main_loop(cur, con):
    #import all scripts and standart libs
    from time import sleep
    from input_values import importv
    from remover import remove
    from rescanner import rescan
    
    #import all important path variables, and set pattern for barcodes
    pattern=r'[0-9]{5}\-[0-9]{7}_[0-9]{4}_[0-9]{1}_[a-zA-z]'
    days, scanfolder, donefolder, oldfolder, problemfolder, logsfolder, delay,repeat_time,check_word =importv()




    #TO_ENABLE MULTIPROCESSING
    #from scanner import scan_run
    #scan_run(scanfolder, donefolder,oldfolder,problemfolder,logsfolder,delay,pattern)

    #TO_ENABLE ONEPROCESSING
    from scanner_one_process import scan
    scan(scanfolder, donefolder,oldfolder,problemfolder,logsfolder,delay,pattern)
    rescan(donefolder,problemfolder,logsfolder,check_word,pattern,cur, con)





    from datetime import datetime, time
    import pytz
    now = datetime.now(pytz.timezone('Europe/Kyiv'))
    now_time = now.time()

    if now_time >= time(6,30) and now_time <= time(7,30):
        remove(days,donefolder,logsfolder,cur, con)
    else:
        pass
    





    print('Waiting...')
    sleep(60 * repeat_time)  # Sleep for 5 minutes



if __name__=="__main__":
    from PsqlConnect import connect
    cur, con=connect()
    while True:
        run_main_loop(cur, con)