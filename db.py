import psycopg2

con = psycopg2.connect(
    database="part4_dev",
    user="part4",
    password="part4_GfhjkzYtn321",
    host="116.203.219.63",
    # host="localhost",
    port="5432"
)

cur = con.cursor()


def i_request(q):
    # print(q)
    try:
        cur.execute(q)
        data = cur.fetchall()
    except psycopg2.DatabaseError as err:
        # if err.pgerror:
        #     print("Error: ", err)
        #     print("Query: ", q)
        pass
    else:
        return data
    finally:
        con.commit()
    # cur.execute(q)
    # data = cur.fetchall()
    # con.commit()
    # return data
