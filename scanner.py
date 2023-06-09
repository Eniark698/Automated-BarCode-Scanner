def scan(scanfolder, donefolder,oldfolder,problemfolder,logsfolder,delay,pattern):

    #exit from another instance, if two times script was started
    from tendo import singleton
    from sys import exit
    try:
        me = singleton.SingleInstance()
    except:
        print("Already running")
        exit(-1)

    from os import mkdir, listdir, getpid, stat, path, remove
    from psutil import Process
    from shutil import move,copy
    from PIL import Image
    Image.MAX_IMAGE_PIXELS = 100000000
    from pyzbar import pyzbar
    from time import time
    from datetime import datetime, timedelta
    from random import random, seed
    from traceback import format_exc
    import re

    failed=0

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
         id varchar(200)
        ,BarCode varchar(200)
        ,location varchar(400)
        ,dateandtime timestamp
        ,storage_inbytes bigint
        ,BarCodeType varchar(50)
        ,direction varchar(1)
        ,is_rescanned boolean);""")
    con.commit()

    #unique seed for random lib
    seed(hash(str(datetime.now())))



    #get list of files in scanfoler
    list=listdir(scanfolder)
    total, j, Mem = 0 , 0 , []


   #procces that files
    try:
        for i in list:
            start_time = time()

            now_date=datetime.now()
            delta=timedelta(minutes=delay)
            c_time=datetime.fromtimestamp(path.getmtime(scanfolder + str(i)))
            if now_date-c_time>delta:
                pass
            else:
                continue



            #if file can not be opened(not a photo), move to problem folder
            try:
                image = Image.open(scanfolder + str(i))
            except:
                copy(scanfolder + str(i), problemfolder + str(i))
                remove(scanfolder + str(i))
                j+=1
                continue

            #get format and size of photo
            format=image.format
            size=stat(scanfolder + str(i)).st_size
            codes=[]


            #get all barcodes from photo
            decoded_objects = pyzbar.decode(image)
            for obj in decoded_objects:
                answer=obj.data.decode()
                typecode=obj.type
                codes.append((answer,typecode))
            image.close()


            #if no codes was detected, move to problem folder
            if codes == []:
                copy(scanfolder + str(i), problemfolder + str(i))
                remove(scanfolder + str(i))
                j+=1
                continue


            #iterator thought all barcodes
            for (answer,typecode) in codes:
                if answer=='' or answer is None:
                    continue
                answer=str(answer)
                r=random()
                h=str(hash(r))
                h=h[:3]

                if re.match(pattern, answer)==None:
                    copy(scanfolder + str(i), problemfolder + str(i))
                    remove(scanfolder + str(i))
                    j+=1
                    continue

                else:
                    pass




                direction=answer[-1]
                direction=direction.lower()
                #if barcode in type code128, then last symbol is direction of sales

                #for code128, with correct ending
                if  typecode=='CODE128' and (direction in ['F', 'f', 'N', 'n']):
                    answer=answer[:-2]
                    name = answer + ',' + h + '.' + format



                    #datn=str(datetime.now())
                    datn=str(now_date)


                    #insert all info about scan in DB
                    cur.execute("""insert into scantable values ('{}','{}','{}','{}',{},'{}','{}','{}');""".format(
                                    name
                                    ,answer
                                    ,donefolder + direction + '/' + answer + '/' + name
                                    ,datn
                                    ,str(size)
                                    ,typecode
                                    ,direction
                                    ,False))


                    #try to make folder with code128 name
                    try:
                        mkdir(donefolder + direction + '/' + answer)
                    except:
                        pass

                    #copy scan into folder
                    copy(scanfolder + str(i)
                        ,donefolder + direction + '/' + answer + '/' + name)
                    remove(scanfolder + str(i))


                    #commit inserting into DB
                    con.commit()
                    break


                #all correct code39 and ean13 into oldefolder
                elif (len(answer)==13 and typecode== 'EAN13') or typecode== 'CODE39':
                    name = answer + ',' + h + '.' + format
                    copy(scanfolder + str(i)
                        ,oldfolder + name)
                    remove(scanfolder + str(i))
                    break



                #any else into problem folder
                else:
                    copy(scanfolder + str(i), problemfolder + str(i))
                    remove(scanfolder + str(i))
                    break


            #get info about time and memory in current itaration
            total+= time() - start_time
            process = Process(getpid())
            Mem.append(process.memory_info().rss/1024/1024)
            j+=1



    #if error, write to log file
    except:
        failed=1
        f=open(logsfolder + 'log_scan.txt', 'a')
        f.write('----------------------------------------\n')
        f.write(format_exc())
        f.write('\nstopped on : '+ str(i) + ' element \n')
        f.write('occurred on ' + str(datetime.now())+ '\n')
        f.write('----------------------------------------\n\n\n')
        f.close()


    # #get info about loop
    # finally:
    #     try:
    #         cur.execute("""create table if not exists monitortable(
    #         dateandtime timestamp
    #         ,Avg_memory_cons float
    #         ,Max_memory_cons float
    #         ,Total_time_of_exec float
    #         ,Number_of_scanned_obj int
    #         ,Avg_time_per_obj float
    #         ,Failed boolean
    #         ,is_rescanned boolean );""")





    #         try:
    #             #at least one file was scanned
    #             max=0
    #             s=0
    #             for i in Mem:
    #                 s+=i
    #                 if i>max:
    #                     max=i

    #             sql_insert_query_monitor  = """
    #                                 INSERT INTO your_table_name (double_column, another_column)
    #                                 VALUES (%s, %s)
    #                                 """


    #             values_to_insert=(
    #                             datetime.now()
    #                             ,s/len(Mem)
    #                             ,max
    #                             ,total
    #                             ,j
    #                             ,total/j
    #                             ,failed
    #                             ,False)


    #             cur.execute(sql_insert_query_monitor, values_to_insert)
    #             con.commit()

    #         except:
    #             #none files was scanned
    #             values_to_insert=( datetime.now()
    #                             ,None
    #                             ,None
    #                             ,None
    #                             ,None
    #                             ,None
    #                             ,failed
    #                             ,False)
    #             cur.execute(sql_insert_query_monitor, values_to_insert)




    #         con.commit()



    #     except:
    #         f=open(logsfolder + 'log_scan.txt', 'a')
    #         f.write('----------------------------------------\n')
    #         f.write(format_exc())
    #         f.write('\nstopped on : '+ str(i) + ' element \n')
    #         f.write('occurred on ' + str(datetime.now())+ '\n')
    #         f.write('----------------------------------------\n\n\n')
    #         f.close()


    #exit
    try:
        cur.close()
        con.close()
    except:
        pass
