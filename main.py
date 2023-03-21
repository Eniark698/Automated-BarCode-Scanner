import os,psutil
import shutil
from distutils.dir_util import copy_tree
from PIL import Image
from pyzbar import pyzbar
#import time
import re
Image.MAX_IMAGE_PIXELS = 1000000000



try:
    shutil.rmtree('/home/parallels/Downloads/Processed/done')
    os.mkdir('/home/parallels/Downloads/Processed/done')
    shutil.rmtree('/home/parallels/Downloads/Processed/not done')
    os.mkdir('/home/parallels/Downloads/Processed/not done')
except:
    print('directories not created')

try:
    shutil.rmtree('/home/parallels/Downloads/scans')
    copy_tree('/home/parallels/Downloads/backup', '/home/parallels/Downloads/scans')
except:
    print('can not remove and copy dir "scans"')

A={}
B={}
i=0
try:
    while True:
        i+=1
        #start_time = time.time()
        image = Image.open('/home/parallels/Downloads/scans/{}.png'.format(str(i)))

        decoded_objects = pyzbar.decode(image)
        for obj in decoded_objects:
            answer=obj.data.decode()
        B[i]=answer
        answer=re.sub('\D', '', answer)
        if len(answer)==13:
            A[i]=answer
            shutil.move('/home/parallels/Downloads/scans/{}.png'.format(i), '/home/parallels/Downloads/Processed/done/{}.png'.format(i))
        else:
            shutil.move('/home/parallels/Downloads/scans/{}.png'.format(i), '/home/parallels/Downloads/Processed/not done/{}.png'.format(i))
        #print("--- %s seconds ---" % (time.time() - start_time))
except:
    print('it was iteration: '+ str(i))
finally:
    print(A)
    print(B)
    process = psutil.Process(os.getpid())
    print(process.memory_info().rss/1024/1014, '- mb')
    quit()



