def scan(scanfolder, donefolder, oldfolder, problemfolder, delay, pattern):
    # exit from another instance, if two times script was started
    from os import mkdir, listdir, stat, path, remove
    from shutil import copy
    from PIL import Image

    Image.MAX_IMAGE_PIXELS = 100000000
    from pyzbar import pyzbar
    from time import time
    from datetime import datetime, timedelta
    from random import random, seed
    import re
    import pytz

  
    import psycopg2
    # con = psycopg2.connect(
    #     host="postgres", database="customs", user="operator", password="ad-fkd342o5-pk3262"
    # )
    con = psycopg2.connect(
        host="localhost", database="postgres", user="postgres", password="frgthy"
    )
    
    # con.autocommit = True
    cur = con.cursor()

    

    

    

    # unique seed for random lib
    seed(hash(str(datetime.now(pytz.timezone('Europe/Kyiv')))))

    j=0

    
    for ter, scanfolder_location in scanfolder.items():
        # get list of files in scanfoler
        list = listdir(scanfolder_location)
        for i in list:

            



            now_date = datetime.now(pytz.timezone('Europe/Kyiv'))
            

            delta = timedelta(minutes=delay)
            c_time = datetime.fromtimestamp(
                path.getmtime(scanfolder_location + str(i)), pytz.timezone("Europe/Kyiv")
            )
            if now_date - c_time > delta:
                pass
            else:
                continue

            # if file can not be opened(not a photo), move to problem folder
            try:
                image = Image.open(scanfolder_location + str(i))
            except:
                copy(scanfolder_location + str(i), problemfolder[ter] + str(i))
                remove(scanfolder_location + str(i))
                j += 1
                continue

            # get format and size of photo
            format = image.format
            size = stat(scanfolder_location + str(i)).st_size
            codes = []

            # get all barcodes from photo
            decoded_objects = pyzbar.decode(image)
            for obj in decoded_objects:
                answer = obj.data.decode()
                typecode = obj.type
                codes.append((answer, typecode))
            image.close()

            # if no codes was detected, move to problem folder
            if codes == []:
                copy(scanfolder_location + str(i), problemfolder[ter] + str(i))
                remove(scanfolder_location + str(i))
                j += 1
                continue

            # iterator thought all barcodes
            for answer, typecode in codes:
                if answer == "" or answer is None:
                    continue
                answer = str(answer)
                r = random()
                h = str(hash(r))
                h = h[:3]

                if re.match(pattern, answer) == None:
                    copy(scanfolder_location + str(i), problemfolder[ter] + str(i))
                    remove(scanfolder_location + str(i))
                    j += 1
                    continue

                else:
                    pass

                direction = answer[-1]
                direction = direction.lower()
                # if barcode in type code128, then last symbol is direction of sales

                # for code128, with correct ending
                if typecode == "CODE128" and (direction in ["F", "f", "N", "n"]):
                    answer = answer[:-2]
                    name = answer + "," + h + "." + format

                    # datn=str(datetime.now())
                    datn = str(now_date)

                    # insert all info about scan in DB
                    cur.execute(
                        """insert into scantable values ('{}','{}','{}','{}',{},'{}','{}','{}','{}');""".format(
                            name,
                            answer,
                            'F:/proc/done/' + direction + "/" + answer + "/" + name,
                            datn,
                            str(size),
                            typecode,
                            direction,
                            False,
                            ter,
                        )
                    )

                    # try to make folder with code128 name
                    try:
                        mkdir(donefolder + direction + "/" + answer)
                    except:
                        pass

                    # copy scan into folder
                    copy(
                        scanfolder_location + str(i),
                        donefolder + direction + "/" + answer + "/" + name,
                    )
                    remove(scanfolder_location + str(i))

                    # commit inserting into DB
                    con.commit()
                    break

                # all correct code39 and ean13 into oldefolder
                elif (
                    len(answer) == 13 and typecode == "EAN13"
                ) or typecode == "CODE39":
                    name = answer + "," + h + "." + format
                    copy(scanfolder_location + str(i), oldfolder + name)
                    remove(scanfolder_location + str(i))
                    break

                # any else into problem folder
                else:
                    copy(scanfolder_location + str(i), problemfolder[ter] + str(i))
                    remove(scanfolder_location + str(i))
                    break

            
            j += 1
    cur.close()
    con.close()
    print('Scanned:  ', j)
    

def scan_run(scanfolder, donefolder, oldfolder, problemfolder, logsfolder, delay, pattern):
    try:
        from multiprocessing import Process
        from traceback import format_exc
        from datetime import datetime
        num_processes = 11
        

        # Create 10 separate processes
        processes = []
        for (key1, value1), (key2,value2) in zip(scanfolder.items(), problemfolder.items()):
            args=({key1:value1}, donefolder, oldfolder, {key2:value2}, delay, pattern)
            p = Process(target=scan, args=(args,))
            processes.append(p)
        
        # Start all the processes
        for p in processes:
            p.start()
        
        # Wait for all processes to complete
        for p in processes:
            p.join()



        print('Finished all subprocess with scan functions')
    except:
        f = open(logsfolder + "log_scan.txt", "a")
        f.write("----------------------------------------\n")
        f.write(format_exc())
        f.write("occurred on " + str(datetime.now()) + "\n")
        f.write("----------------------------------------\n\n\n")
        f.close()

