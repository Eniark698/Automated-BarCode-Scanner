def scan(scanfolder, donefolder,oldfolder,problemfolder,logsfolder):

    #exit from another instance, if two times script was started
    from tendo import singleton
    from sys import exit
    try:
        me = singleton.SingleInstance()
    except:
        print("Already running")
        exit(-1)

    from os import mkdir, listdir, getpid, stat, remove
    from psutil import Process
    from shutil import copy,move
    from PIL import Image
    Image.MAX_IMAGE_PIXELS = 100000000
    from pyzbar import pyzbar
    from time import time
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
        ,direction varchar(1));""")
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


            #if file can not be opened(not a photo), move to problem folder
            try:
                image = Image.open(scanfolder + str(i))
            except:
                move(scanfolder + str(i), problemfolder + str(i))
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

            #if no codes was detected, move to problem folder
            if codes == []:
                move(scanfolder + str(i), problemfolder + str(i))
                j+=1
                continue


            #iterator thought all barcodes
            for (answer,typecode) in codes:
                answer=str(answer)
                r=random()
                h=str(hash(r))
                h=h[:3]
                direction=answer[-1]
                direction=direction.lower()
                #if barcode in type code128, then last symbol is direction of sales

                #for code128, with correct ending
                if  typecode=='CODE128' and (direction in ['F', 'f', 'N', 'n']):
                    answer=answer[:-2]
                    name = answer + ',' + h + '.' + format


                    #try to make folder with code128 name
                    try:
                        mkdir(donefolder + direction + '/' + answer)
                    except:
                        pass


                    
                    datn=str(datetime.now())



                    #insert all info about scan in DB
                    cur.execute("""insert into scantable values ('{}','{}','{}','{}',{},'{}','{}');""".format(
                                    name
                                    ,answer
                                    ,donefolder + name
                                    ,datn
                                    ,str(size)
                                    ,typecode
                                    ,direction))

                    #copy scan into folder
                    copy(scanfolder + str(i)
                        ,donefolder + direction + '/' + answer + '/' + name)

                    #commit inserting into DB
                    con.commit()


                #all correct code39 and ean13 into oldefolder
                elif (len(answer)==13 and typecode== 'EAN13') or typecode== 'CODE39':
                    name = answer + ',' + h + '.' + format
                    copy(scanfolder + str(i)
                        ,oldfolder + name)



                #any else into problem folder
                else:
                    copy(scanfolder + str(i), problemfolder + str(i))
            remove(scanfolder + str(i))


            #get info about time and memory in current itaration
            total+= time() - start_time
            process = Process(getpid())
            Mem.append(process.memory_info().rss/1024/1024)
            j+=1



    #if error, write to log file
    except:
        f=open(logsfolder + 'log_scan.txt', 'a')
        f.write('----------------------------------------\n')
        f.write(format_exc())
        f.write('\nstopped on : '+ str(j/len(list)*100) + ' %\n')
        f.write('occurred on ' + str(datetime.now())+ '\n')
        f.write('----------------------------------------\n\n\n')
        f.close()


    #get info about loop
    else:
        try:
            max=0
            s=0
            for i in Mem:
                s+=i
                if i>max:
                    max=i
            print('Avg memory cons.: ' + str(s/len(Mem)) + ' - mb')
            print('Max memory cons.: ' + str(max) + ' - mb')
            print('Total time of exec: ' + str(total) + ' - sec')
            print('Number of scanned obj: ' + str(j))
            print('Avg time per obj: ' + str(total/j) + ' - sec/obj')
        except:
            print('none files was scanned')

    finally:
        cur.close()
        con.close()
