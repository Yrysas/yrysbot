import psycopg2


con = psycopg2.connect(
    database="telegram_db",
    user = "postgres",
    password = "postgres",
    host = "127.0.0.1",
    port = "5432"
)

cur = con.cursor()


def newJob( myName, muMesage, myNomer, myTime):
    sql = "INSERT INTO users ( name, nomer, message, time) VALUES ( %s, %s,%s,%s)"
    val = (myName, myNomer, muMesage, myTime)
    cur.execute(sql, val)
    con.commit()

def mySeanss(var):
    sql = "SELECT * FROM users WHERE name = %s"
    val = (var,)
    cur.execute(sql, val)
    q = cur.fetchall()
    return q


con.commit()

