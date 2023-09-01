def connect():    

    import psycopg2
    # con = psycopg2.connect(
    #     host="postgres", database="customs", user="operator", password="ad-fkd342o5-pk3262"
    # )
    con = psycopg2.connect(
        host="postgres", database="postgres", user="postgres", password="frgthy"
    )
    
    # con.autocommit = True
    cur = con.cursor()
    cur.execute(
        """create table if not exists scantable(
        id varchar(200)
        ,BarCode varchar(200)
        ,location varchar(400)
        ,dateandtime timestamp
        ,storage_inbytes bigint
        ,BarCodeType varchar(50)
        ,direction varchar(1)
        ,is_rescanned boolean
        ,territory varchar(100));"""
    )
    con.commit()
    return cur, con