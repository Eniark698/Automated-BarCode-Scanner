def remove():
    from os import listdir
    from datetime import datetime
    from shutil import rmtree

    def days_between(d1, d2):
        d1 = datetime.strptime(d1, "%Y-%m-%d")
        d2 = datetime.strptime(d2, "%Y-%m-%d")
        return abs((d2 - d1).days)

    now_date=datetime.today().strftime('%Y-%m-%d')

    path='/home/parallels/Downloads/'

    list=listdir(path + ('Processed/done/'))
    for i in list:
        if abs(days_between(now_date,i))>100:
            rmtree(path + 'Processed/done/{}'.format(i))

remove()
