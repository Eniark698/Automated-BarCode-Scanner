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
    from sqlite3 import connect
    from random import random, seed

    Image.MAX_IMAGE_PIXELS = 1000000000

    seed(hash(datetime.today().strftime('%Y-%m-%d')))

    ###############################
    #your path
    global path
    path='/home/parallels/Downloads/'

    ###############################

    con=connect(path + ('scandata.db'))
    cur=con.cursor()
    cur.execute("""create table if not exists scantable(
        id varchar(100)
        ,BarCod varchar(100)
        ,location varchar(200)
        ,dateandtime varchar(100)
        ,storage_inbytes int64
        ,BarCodType varchar(100))""")

    list=listdir(path + ('scans/'))

    total=0
    j=0
    Mem=[]
    date=datetime.today().strftime('%Y-%m-%d')

    try:
        mkdir(path + ('Processed/done/{}'.format(date)))
    except:
        pass

    try:
        for i in list:
            codes=[]
            start_time = time()
            try:
                image = Image.open(path + ('scans/{}'.format(i)))
            except:
                move(path + ('scans/{}'.format(i)), path + ('Processed/not done/{}'.format(i)))
                j+=1
                continue
            format=image.format

            size=stat(path + ('scans/{}'.format(i))).st_size

            decoded_objects = pyzbar.decode(image)
            for obj in decoded_objects:
                answer=obj.data.decode()
                typecode=obj.type
                codes.append((answer,typecode))

            #answer1=answer
            #answer=sub('\D', '', answer)

            for (answer,typecode) in codes:

                r=random()
                h=hash(r)

                if (((len(answer)==13 and typecode== 'EAN13')
                     or typecode=='CODE39'
                     or typecode=='CODE128')
                    and answer!=''):

                    copy(path + ('scans/{}'.format(i))
                        ,path + ('Processed/done/{}/{}.{}'.format(date,h,format)))
                    s="""insert into scantable values ('{}','{}','{}','{}',{},'{}')""".format(
                                    str(h)
                                    ,str(answer)
                                    ,path + ("Processed/done/{}/{}.{}".format(date,h,format))
                                    ,date
                                    ,str(size)
                                    ,typecode)
                    con.execute(s)
                    con.commit()
                else:
                    copy(path + ('scans/{}'.format(i)), path + ('Processed/not done/{}.{}'.format(h,format)))
            remove(path + ('scans/{}'.format(i)))
            total+= time() - start_time
            #print("--- %s seconds ---" % (time() - start_time))

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
            print('not completed scanning')
            print('\nstopped on : '+ str(j/len(list)*100) + ' %\n')


scan()
