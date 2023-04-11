def remove():
    from os import listdir
    from datetime import datetime
    from shutil import rmtree
    import json

    def days_between(d1, d2):
        d1 = datetime.strptime(d1, "%Y-%m-%d")
        d2 = datetime.strptime(d2, "%Y-%m-%d")
        return abs((d2 - d1).days)

    now_date=datetime.today().strftime('%Y-%m-%d')

    path='F:\project/'


    with open(path + 'config.json') as json_file:
        data = json.load(json_file)
        try:
            days=data["days_to_remove"]
        except Exception as err:
            days=100
            f=open(path + 'log_conf.txt', 'a')
            f.write('--\n')
            f.write(str(Exception))
            f.write('\n')
            f.write(str(err))
            f.write('occurred on ' + str(datetime.now()))
            f.write('\n--\n\n\n')
            f.close()

    list=listdir(path + ('Processed/done/'))
    for i in list:
        if abs(days_between(now_date,i))>days:
            rmtree(path + 'Processed/done/{}'.format(i))

remove()
