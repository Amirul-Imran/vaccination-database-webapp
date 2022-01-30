import numpy as np
import sqlite3
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def db_connect():
    db = sqlite3.connect("vaccine.db")
    c = db.cursor()

    table = c.execute("""SELECT name FROM sqlite_master WHERE type='table'
                            AND name='students'; """).fetchall()

    if not table:
        c.execute("""CREATE TABLE students ( 
                name text,
                id int,
                dept int, 
                vaccine int)""")

        db.commit()
    return db


def create_plot():
    no_shots = [0, 0, 0, 0, 0, 0]
    one_shot = [0, 0, 0, 0, 0, 0]
    two_shots = [0, 0, 0, 0, 0, 0]

    conn = db_connect()
    c = conn.cursor()
    items = c.execute("SELECT * FROM students").fetchall()

    for item in items:
        if item[3] == 0:
            no_shots[item[2]] += 1
            no_shots[0] += 1
        elif item[3] == 1:
            one_shot[item[2]] += 1
            one_shot[0] += 1
        else:
            two_shots[item[2]] += 1
            two_shots[0] += 1

    sub = ['Total', 'Mechanical', 'Electrical', 'Chemical', 'Civil', 'Biomedical']

    height = 0.15
    values = np.arange(len(sub))
    plt.barh(values + height + height, no_shots, height, label='No Vaccination')
    plt.barh(values + height, one_shot, height, label='One Dose')
    plt.barh(values, two_shots, height, label='Two Doses')

    plt.xlabel('Number of Students')
    plt.title('Vaccination Chart')
    plt.legend()
    plt.yticks(values + height, sub)
    plt.tight_layout()
    plt.savefig("static/stats.jpg")
    plt.plot()
    plt.clf()
    conn.close()
