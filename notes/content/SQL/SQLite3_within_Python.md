## SQLite3 within Python

### Closing connections explicitly

Even though connections are supposedly closed automatically, doing so explicitly with

    object.connection.commit()
    object.cursor.close()
    object.connection.close()

 is safer.

### Basic instructions used

    import sqlite3
    con = sqlite3.connect('test.db')
    # use con = sqlite3.connect(":memory:") to create the db in RAM!
    curs = con.cursor()
    con.close()

### Short program to find version number

    #!/usr/bin/python
    # -*- coding: utf-8 -*-
    
    import sqlite3
    import sys
    
    con = sqlite3.connect('test.db')
    with con:
        cur = con.cursor()    
        cur.execute('SELECT SQLITE_VERSION()')
        data = cur.fetchone()
        print("SQLite version: {}".format(data[0]))

## Running SQL script within Python


    con = sqlite3.connect('database.db')
    with con:
        curs = con.cursor()
        query = open('script.sql', 'r').read()
        curs.executescript(query)


## Examples

### `fetchall` and `fetchone`

    import sqlite3
    conn = sqlite3.connect('hl.db')
    c = conn.cursor()
    o = c.execute('''SELECT ticker,headline FROM headlines''')
    o.fetchall() # o is then populated with a list of tuples --- one tuple per record

`fetchall()`:

    In [28]: o = c.execute('''SELECT ticker,headline FROM headlines''')

    In [29]: o.fetchone()
    Out[29]: ('VZ', 'junk VZ headline')

    In [30]: o.fetchone()
    Out[30]: ('XOXO', 'junk XOXO headline')

    In [31]: o.fetchone()
    Out[31]: ('TLLP', 'junk TLLP headline')

### Other facts

#### Cannot reset cursor!

    > The SQLite interface in Python 3.1 is based on PEP 249, which only
    > specifies that cursors have to support sequential access to the
    > records of a query result. There’s no way to go back. If you need
    > to return to a previously fetched row, you should save it when you
    > first fetch it, e.g. create a list of the fetched data (or
    > actually, just use `fetchall`). Then you can work with the list
    > and go back and forth between rows as much as you want.
    >
    > The idea behind the design of the DB API is to support efficient
    > execution of code where you only need to process each row once.
    
 (http://stackoverflow.com/a/2796571/621762)

 So one must make the database do as much selection as possible before beginning manipulation within Python.


[end]
