#import quantumrandom
#a=maxsize
#b=-maxsize-1
#seed(quantumrandom.randint(0,a))




def scan():
    from tendo import singleton
    from sys import exit
    try:
        me = singleton.SingleInstance()
    except:
        print("Already running")
        exit(-1)

    from os import mkdir, listdir, getpid, stat, remove
    from psutil import Process
    from shutil import copy,move,rmtree
    from distutils.dir_util import copy_tree
    from PIL import Image
    from pyzbar import pyzbar
    from time import time, sleep
    from datetime import datetime
    from re import sub
    from random import random, seed

    import psycopg2
    con = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="$confident$")
    con.autocommit = True
    cur = con.cursor()
    cur.execute("""create table if not exists scantable(
        id varchar(50)
        ,BarCod varchar(50)
        ,location varchar(200)
        ,dateandtime timestamp
        ,storage_inbytes bigint
        ,BarCodType varchar(100));""")

    Image.MAX_IMAGE_PIXELS = 1000000000
    date=datetime.today().strftime('%Y-%m-%d')
    seed(hash(date))

    ###############################
    #your path
    global path
    path='F:\project/'
    ###############################

    list=listdir(path + ('scans/'))
    total, j, Mem = 0 , 0 , []


    try:
        mkdir(path + ('Processed/done/{}'.format(date)))
    except:
        pass

    try:
        for i in list:
            start_time = time()

            try:
                image = Image.open(path + ('scans/{}'.format(i)))
            except:
                move(path + ('scans/{}'.format(i)), path + ('Processed/with problem/{}'.format(i)))
                j+=1
                continue

            format=image.format
            size=stat(path + ('scans/{}'.format(i))).st_size
            codes=[]

            decoded_objects = pyzbar.decode(image)
            for obj in decoded_objects:
                answer=obj.data.decode()
                typecode=obj.type
                codes.append((answer,typecode))

            for (answer,typecode) in codes:
                r=random()
                h=hash(r)

                if len(answer)==13 and (typecode== 'EAN13' or typecode== 'CODE39'):
                    # or typecode=='CODE128'

                    copy(path + ('scans/{}'.format(i))
                        ,path + ('Processed/done/{}/{}.{}'.format(date,h,format)))
                    cur.execute("""insert into scantable values ('{}','{}','{}','{}',{},'{}');""".format(
                                    str(h)
                                    ,str(answer)
                                    ,path + ("Processed/done/{}/{}.{}".format(date,h,format))
                                    ,date
                                    ,str(size)
                                    ,typecode))
                else:
                    copy(path + ('scans/{}'.format(i)), path + ('Processed/not done/{}.{}'.format(h,format)))
            remove(path + ('scans/{}'.format(i)))

            total+= time() - start_time
            process = Process(getpid())
            Mem.append(process.memory_info().rss/1024/1024)
            j+=1

    except Exception as err:
        f=open(path + 'log.txt', 'a')
        f.write('--\n')
        f.write(str(Exception))
        f.write('\n')
        f.write(str(err))
        f.write('\nstopped on : '+ str(j/len(list)*100) + ' %\n')
        f.write('occurred on ' + str(datetime.now()))
        f.write('\n--\n\n\n')
        f.close()

    finally:
        if j!=0:
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

        else:
            print('no file was scanned')

    cur.close()
    con.close()

scan()
