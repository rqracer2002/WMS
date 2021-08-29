
import sqlite3

def myname(orderheader):

        print("The POD is related to order header "+orderheader)
        con = sqlite3.connect('C:\\Users\\Rafael\\Desktop\\WMS\\db.sqlite3')

        cur = con.cursor()

        # Create table
        # cur.execute('''CREATE TABLE stocks
        #                (date text, trans text, symbol text, qty real, price real)''')
        # Insert a row of data
        cur.execute("Update blog_orderheader set pod = ? where id = ?",("Yes",orderheader))
        cur.execute("Update blog_orderheader set submit = ? where id = ?",("",orderheader))

        # insert into blog_orderdetail values (3,1,96,'47317-38/00207',10,0);

        # Save (commit) the changes
        con.commit()

        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        con.close()

def myvalidator(mymodel_id):
    mylist = []
    print("Validating if POD has been submitted already for order "+ mymodel_id)
    con = sqlite3.connect('C:\\Users\\Rafael\\Desktop\\WMS\\db.sqlite3')

    cur = con.cursor()


    cur.execute("select * from blog_mymodel where orderheader_id = ?",(mymodel_id,))

    rows = cur.fetchall()

    for row in rows:

#         print(row)

        mylist.append(row)

        print(mylist)


    if len(mylist) == 0:
        return "valid"

    else:
        return "invalid"



        # insert into blog_orderdetail values (3,1,96,'47317-38/00207',10,0);



        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        con.close()
