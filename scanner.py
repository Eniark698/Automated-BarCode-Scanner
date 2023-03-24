def main():
    from tendo import singleton
    from sys import exit
    try:
        me = singleton.SingleInstance()
    except:
        print("Already running")
        exit(-1)

    from os import mkdir, listdir, getpid, stat
    from psutil import Process
    from shutil import move,rmtree
    from distutils.dir_util import copy_tree
    from PIL import Image
    from pyzbar import pyzbar
    from time import time, sleep
    from datetime import datetime
    from re import sub
    from sqlite3 import connect
    Image.MAX_IMAGE_PIXELS = 1000000000

    con=connect('/home/parallels/Downloads/scandata.db')
    cur=con.cursor()
    cur.execute('create table if not exists scantable(id int64, location nvarchar(200), dateandtime varchar(100), storage_inbytes int64)')

    list=listdir('/home/parallels/Downloads/scans/')

    total=0
    j=0
    Mem=[]


    try:
        for i in list:

            start_time = time()
            try:
                image = Image.open('/home/parallels/Downloads/scans/{}'.format(i))
            except:
                move(r'/home/parallels/Downloads/scans/{}'.format(i), r'/home/parallels/Downloads/Processed/not done/{}.withproblem'.format(i))
                j+=1
                continue
            format=image.format

            size=stat('/home/parallels/Downloads/scans/{}'.format(i)).st_size

            decoded_objects = pyzbar.decode(image)
            for obj in decoded_objects:
                answer=obj.data.decode()
            answer1=answer
            answer=sub('\D', '', answer)
            if len(answer)==13:
                move('/home/parallels/Downloads/scans/{}'.format(i), '/home/parallels/Downloads/Processed/done/{}.{}'.format(answer,format))
                s="""insert into scantable values ({},'{}','{}',{})""".format(
                                    str(answer)
                                   ,"/home/parallels/Downloads/Processed/done/{}.{}".format(answer,format)
                                   ,datetime.now()
                                   ,str(size))
                con.execute(s)
                con.commit()
            else:
                move('/home/parallels/Downloads/scans/{}'.format(i), '/home/parallels/Downloads/Processed/not done/{}.{}'.format(answer1,format))

            total+= time() - start_time
            #print("--- %s seconds ---" % (time() - start_time))

            process = Process(getpid())
            Mem.append(process.memory_info().rss/1024/1024)
            j+=1

    except Exception as err:
        f=open('/home/parallels/Documents/log.txt', 'a')
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
            print('Zero objects scanned')
            print('\nstopped on : '+ str(j/len(list)*100) + ' %\n')

main()




