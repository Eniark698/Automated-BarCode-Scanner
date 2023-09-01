def rescan(donefolder, problemfolder, logsfolder, check_word, pattern,cur, con):
    from tendo import singleton
    from sys import exit

    try:
        me = singleton.SingleInstance()
    except:
        print("Already running")
        exit(-1)

    from os import mkdir, listdir, stat, remove
    from shutil import copy, move
    from PIL import Image

    Image.MAX_IMAGE_PIXELS = 100000000
    from datetime import datetime, timezone,timedelta
    from random import random, seed
    from traceback import format_exc
    import re
    import pytz
    
    # unique seed for random lib
    seed(hash(str(datetime.now(pytz.timezone('Europe/Kyiv')))))

    j = 0
    check_len = len(check_word) + 1
    format = "JPEG"

    try:
        # for all files in problem folder
        for iter in range(len(problemfolder)):
            # get all filenames in problem folder
            list = listdir(problemfolder[iter])

            match iter:

                case 0:
                    ter='Lviv'
                case 1:
                    ter='Mukachevo'
                case 2:
                    ter='Sambir'
                case 3:
                    ter='Ternopil'
                case 4:
                    ter='Vinnytsia'
                case 5:
                    ter='Zhytomyr'
                case 6:
                    ter='Rivne'
                case 7:
                    ter='Lutsk'
                case 8:
                    ter='Khmelnytskyi'
                case 9:
                    ter='Frankivsk'
                case 10:
                    ter='Chernivtsi'


            for i in list:
                size = None

                # check if filename startswith control symbols
                if i.startswith(check_word):
                    j += 1
                    # try to open photo to get format and size
                    try:
                        image = Image.open(problemfolder[iter] + str(i))
                        image.close()
                        size = str(stat(problemfolder[iter] + str(i)).st_size)
                    except:
                        pass

                    # try to find dot in name to get extention of file
                    try:
                        pos = i.find(".")
                        answer = i[check_len:pos]
                    except:
                        answer = i[check_len:]

                    # get random 3 symbols to unique file, get direction of sales
                    r = random()
                    h = str(hash(r))
                    h = h[:3]

                    if re.match(pattern, answer) == None:
                        continue
                    else:
                        pass

                    direction = answer[-1]
                    direction = direction.lower()
                    datn = str(datetime.now(pytz.timezone('Europe/Kyiv')))
                    answer = answer[:-2]
                    name = answer + "," + h + "." + format

                    if direction not in ("f", "n"):
                        continue

                    # insert into DB
                    cur.execute(
                        """insert into scantable values ('{}','{}','{}','{}',{},'{}','{}','{}','{}');""".format(
                            name,
                            answer,
                            'F:/proc/done/' + direction + "/" + answer + "/" + name,
                            datn,
                            size,
                            None,
                            direction,
                            True,
                            ter,
                        )
                    )

                    # try to make folder with barcode name
                    try:
                        mkdir(donefolder + direction + "/" + answer)
                    except:
                        pass

                    # copy file into folder
                    try:
                        copy(
                            problemfolder[iter] + str(i),
                            donefolder + direction + "/" + answer + "/" + name,
                        )
                        remove(problemfolder[iter] + str(i))
                    except:
                        con.rollback()
                        continue

                    # commit inserting into DB
                    con.commit()

                else:
                    continue

                size = None
    # write if error has occurred
    except:
        f = open(logsfolder + "log_rescan.txt", "a")
        f.write("----------------------------------------\n")
        f.write(format_exc())
        f.write("\nstopped on : " + str(i) + " file\n")
        f.write("occurred on " + str(datetime.now()) + "\n")
        f.write("----------------------------------------\n\n\n")
        f.close()

    # exit
    print(j, " files was rescanned")
  