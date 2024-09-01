import timeit
import datetime
from multiprocessing import Pool
import sqlite3
import hashlib

import numpy as np

def f(x):
    return x**x

def wrapper(x):
    # x = hashlib.sha512(str(x).encode())
    # for j in range(10**4):
    #     x = hashlib.sha512(str(x).encode())
    x= x[-1]
    x = int(x, 16)
    for j in range(10**5):
        x = x**8 
        x %= (j + 100)**4
    
    return x

if __name__ == '__main__':

    with sqlite3.connect('test.db', autocommit=True) as db, Pool(16) as pool:

        cur = db.cursor()
        # cur.execute("DROP TABLE IF EXISTS test_table")
        cur.execute("""CREATE TABLE IF NOT EXISTS test_table(name TEXT, data TEXT);""")

        # for j in range(10**4):
        #     sha = hashlib.sha512(str(j).encode())
        #     # print(sha.hexdigest())
        #     q = f"""INSERT INTO test_table(name, data) VALUES ({j}, '{str(sha.hexdigest())}');"""
        #     cur.execute(q)
        # db.commit()

        iterable = list(cur.execute("SELECT name, data FROM test_table").fetchall())
        t0 = datetime.datetime.now()    

        # for row in iterable:
        #     wrapper(row[-1])

        for r in pool.imap_unordered(wrapper, iterable):
            pass

        elapsed = datetime.datetime.now() - t0
        print(elapsed.total_seconds())
