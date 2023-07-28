def write(logsfolder):
    import psycopg2
    from  datetime import datetime
    from traceback import format_exc

    try:
        con = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="frgthy")
        #con.autocommit = True
        cur = con.cursor()

        cur.execute('select count(*) from scantable where dateandtime>=now()::date')

        number_str  = cur.fetchall()
        number=number_str[0][0]
        
        f=open(logsfolder + 'total.txt', 'a')
        f.write('----------------------------------------\n')
        f.write('total for today'+ str(number)+'\n')
        f.write('occurred on ' + str(datetime.now())+ '\n')
        f.write('----------------------------------------\n\n\n')
        f.close()
        print('Written: ', int(number))
        cur.close()
        con.close()

    except:
        f1=open(logsfolder + 'log_total.txt', 'a')
        f1.write('----------------------------------------\n')
        f1.write(format_exc())
        f1.write('\noccurred on ' + str(datetime.now())+ '\n')
        f1.write('----------------------------------------\n\n\n')
        f1.close()