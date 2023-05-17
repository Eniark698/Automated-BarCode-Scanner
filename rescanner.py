def rescan(donefolder,problemfolder,logsfolder):
    from tendo import singleton
    from sys import exit
    try:
        me = singleton.SingleInstance()
    except:
        print("Already running")
        exit(-1)

    from os import mkdir, listdir, stat, remove
    from shutil import copy,move
    from PIL import Image
    Image.MAX_IMAGE_PIXELS = 100000000
    from datetime import datetime
    from random import random, seed
    from traceback import format_exc


    #connect to psql, create table if not exists
    import psycopg2
    con = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="frgthy")
    #con.autocommit = True
    cur = con.cursor()
    cur.execute("""create table if not exists scantable(
         id varchar(200) unique
        ,BarCode varchar(200)
        ,location varchar(400)
        ,dateandtime timestamp
        ,storage_inbytes bigint
        ,BarCodeType varchar(50)
        ,direction varchar(1)
        ,is_rescanned bit);""")
    con.commit()

    #unique seed for random lib
    seed(hash(str(datetime.now())))

    #get all filenames in problem folder
    list=listdir(problemfolder)




    try:
        #for all files in problem folder
        
        for i in list:
            format = None
            size = None



            #check if filename startswith control symbols
            if i.startswith('IRIS_'):
                format=''

                #try to open photo to get format and size
                try:
                    image = Image.open(problemfolder + str(i))
                    format=image.format
                    size=str(stat(problemfolder + str(i)).st_size)
                except:
                    pass

                #try to find dot in name to get extention of file
                try:
                    pos=i.find('.')
                    answer=i[5:pos]
                    if format!='':
                        format=i[pos+1:]
                except:
                    answer=i[5:]


                #get random 3 symbols to unique file, get direction of sales
                r=random()
                h=str(hash(r))
                h=h[:3]
                direction=answer[-1]
                direction=direction.lower()
                datn=str(datetime.now())
                answer=answer[:-2]
                name = answer + ',' + h + '.' + format



                
                
                #insert into DB
                cur.execute("""insert into scantable values ('{}','{}','{}','{}',{},'{}','{}','{}');""".format(
                                        name
                                        ,answer
                                        ,donefolder + name
                                        ,datn
                                        ,size
                                        ,None
                                        ,direction
                                        ,1))


                #try to make folder with barcode name
                try:
                    mkdir(donefolder + direction + '/' + answer)
                except:
                    pass



                #copy file into folder
                try:
                    move(problemfolder + str(i)
                        ,donefolder + direction + '/' + answer + '/' + name)
                except:
                    con.rollback()
                    continue
               
                #commit inserting into DB
                con.commit()

            else:
                continue



            format = None
            size = None
    #write if error has occurred
    except:
        f=open(logsfolder + 'log_rescan.txt', 'a')
        f.write('----------------------------------------\n')
        f.write(format_exc())
        f.write('\nstopped on : '+ str(i) + ' file\n')
        f.write('occurred on ' + str(datetime.now())+ '\n')
        f.write('----------------------------------------\n\n\n')
        f.close()

    #exit
    try:
        cur.close()
        con.close()
    except:
        pass

        
    