def scan(scanfolder, donefolder,oldfolder,problemfolder,logsfolder):

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
    from distutils.dir_util import copy_tree
    from PIL import Image
    Image.MAX_IMAGE_PIXELS = 10000000000
    from pyzbar import pyzbar
    from time import time
    from datetime import datetime
    from re import sub
    from random import random, seed
    from traceback import format_exc
   


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
     
    seed(hash(str(datetime.now())))

    

    list=listdir(scanfolder)
    total, j, Mem = 0 , 0 , []
   
    try:
        for i in list:
            start_time = time()

            try:
                image = Image.open(scanfolder + str(i))
            except:
                move(scanfolder + str(i), problemfolder + str(i))
                j+=1
                continue

            format=image.format
            size=stat(scanfolder + str(i)).st_size
            codes=[]

            decoded_objects = pyzbar.decode(image)
            for obj in decoded_objects:
                answer=obj.data.decode()
                typecode=obj.type
                codes.append((answer,typecode))

            if codes == []:
                move(scanfolder + str(i), problemfolder + str(i))
                j+=1
                continue
    

            for (answer,typecode) in codes:
                answer=str(answer)
                r=random()
                h=str(hash(r))
                h=h[:3]
                direction=answer[-1]
                answer=answer[:-2]
               
                

                if  typecode=='CODE128' and (direction in ['F', 'f', 'N', 'n']):

                    direction=direction.lower()
                    datn=str(datetime.now())
                    name = answer + '_' + h + '.' + format

                    try:
                        mkdir(donefolder + direction + '/' + answer)
                    except:
                        pass

                    cur.execute("""insert into scantable values ('{}','{}','{}','{}',{},'{}','{}');""".format(
                                    name
                                    ,answer
                                    ,donefolder + name
                                    ,datn
                                    ,str(size)
                                    ,typecode
                                    ,direction))
                    
                    copy(scanfolder + str(i)
                        ,donefolder + direction + '/' + answer + '/' + name)
                    
                    con.commit()

                elif len(answer)==13 and (typecode== 'EAN13' or typecode== 'CODE39'):
                    copy(scanfolder + str(i)
                        ,oldfolder + str(i)+ '.'+ format)
                    
                    
                else:
                    copy(scanfolder + str(i), problemfolder + str(i))
            remove(scanfolder + str(i))        
            
            
            total+= time() - start_time
            process = Process(getpid())
            Mem.append(process.memory_info().rss/1024/1024)
            j+=1

    except:
        f=open(logsfolder + 'log_scan.txt', 'a')
        f.write('----------------------------------------\n')
        f.write(format_exc())
        f.write('\nstopped on : '+ str(j/len(list)*100) + ' %\n')
        f.write('occurred on ' + str(datetime.now())+ '\n')
        f.write('----------------------------------------\n\n\n')
        f.close()
        

    else:
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

    finally:
        cur.close()
        con.close()

