from django.core.paginator import Paginator
import sqlite3
from models import OrderHeader

def query_orders():
      mylist = []
    con = sqlite3.connect('C:\\Users\\Rafael\\Desktop\\WMS\\db.sqlite3')
    cur = con.cursor()
    cur.execute("select * from blog_orderheader;")
    rows = cur.fetchall()

        for row in rows:
            mylist.append(row)

    return mylist
