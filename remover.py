def remove(days,  donefolder,logsfolder,cur, con):
    from datetime import datetime
    from os import listdir
    import os.path as path
    from traceback import format_exc
    from shutil import rmtree
    
    #function to get difference in days between two dates
    def days_between(d1, d2):
        d1 = datetime.strptime(d1, "%Y-%m-%d")
        d2 = datetime.strptime(d2, "%Y-%m-%d")
        return abs((d2 - d1).days)
    now_date=datetime.today().strftime('%Y-%m-%d')

    


    #try to delete files with scans, if date of modification greater then days_to_delete
    #also, delete from psql DB
    j=0
    try:
        list=listdir(donefolder + 'f/')
        for i in list:
            c_time=datetime.fromtimestamp(path.getmtime(donefolder + 'f/' + i)).strftime('%Y-%m-%d')
            if abs(days_between(now_date,c_time))>=days:
                rmtree(donefolder + 'f/' + i)
                j+=1

        list=listdir(donefolder + 'n/')
        for i in list:
            c_time=datetime.fromtimestamp(path.getmtime(donefolder + 'n/' + i)).strftime('%Y-%m-%d')
            if abs(days_between(now_date,c_time))>=days:
                rmtree(donefolder + 'n/' + i)
                j+=1
        
        
        cur.execute("""delete from scantable where DATE_PART('days', NOW()-dateandtime)>={};""".format(days))
        con.commit()
        

    #in case of error, write to log file
    except:
        f=open(logsfolder + 'log_rem.txt', 'a')
        f.write('----------------------------------------\n')
        f.write(format_exc())
        f.write('occurred on ' + str(datetime.now())+ '\n')
        f.write('----------------------------------------\n\n\n')
        f.close()



    print(j, ' files was removed')
