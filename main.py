from flask import Flask, render_template, url_for, flash, redirect, abort, request
from forms import AddForm, SearchForm, RemoveForm
import numpy as np
import sqlite3
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


app = Flask(__name__)
app.config["SECRET_KEY"] = "c8b49ab7a60dcb042d7d8148617fdf91"


def db_connect():
    db = sqlite3.connect("vaccine.db")
    c = db.cursor()

    table = c.execute("""SELECT name FROM sqlite_master WHERE type='table'
                            AND name='students'; """).fetchall()

    if not table:
        c.execute("""CREATE TABLE students ( 
                name text,
                id int,
                dept text, 
                vaccine int)""")

        db.commit()
    return db


def create_plot():
    n = [0, 0, 0, 0, 0, 0]
    o = [0, 0, 0, 0, 0, 0]
    t = [0, 0, 0, 0, 0, 0]

    conn = db_connect()
    c = conn.cursor()
    items = c.execute("SELECT * FROM students").fetchall()

    for i in items:
        if i[2] == 'Biomedical':
            if i[3] == 0:
                n[5] += 1
            if i[3] == 1:
                o[5] += 1
            if i[3] == 2:
                t[5] += 1

        if i[2] == 'Civil':
            if i[3] == 0:
                n[4] += 1
            if i[3] == 1:
                o[4] += 1
            if i[3] == 2:
                t[4] += 1

        if i[2] == 'Chemical':
            if i[3] == 0:
                n[3] += 1
            if i[3] == 1:
                o[3] += 1
            if i[3] == 2:
                t[3] += 1

        if i[2] == 'Electrical':
            if i[3] == 0:
                n[2] += 1
            if i[3] == 1:
                o[2] += 1
            if i[3] == 2:
                t[2] += 1

        if i[2] == 'Mechanical':
            if i[3] == 0:
                n[1] += 1
            if i[3] == 1:
                o[1] += 1
            if i[3] == 2:
                t[1] += 1

        if i[3] == 0:
            n[0] += 1
        if i[3] == 1:
            o[0] += 1
        if i[3] == 2:
            t[0] += 1

    sub = ['Total', 'ME', 'EE', 'ChE', 'CE', 'BME']

    height = 0.15
    values = np.arange(len(sub))
    plt.barh(values + height + height, n, height, label='No Vaccination')
    plt.barh(values + height, o, height, label='One Dose')
    plt.barh(values, t, height, label='Two Doses')

    plt.ylabel('Department')
    plt.xlabel('Number of Students')
    plt.title('Vaccination Chart')
    plt.legend()
    plt.yticks(values + height, sub)
    plt.savefig("static/stats.jpg")
    plt.plot()
    plt.clf()
    conn.close()


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/add", methods=["GET", "POST"])
def add():
    form = AddForm()
    if form.validate_on_submit():
        conn = db_connect()
        c = conn.cursor()
        student = c.execute("SELECT * FROM students WHERE id=:id", {"id": form.id.data}).fetchone()
        if student is None:
            c.execute("INSERT INTO students VALUES (:name, :id, :dept, :vacc)", {"name": form.name.data, "id": form.id.data, "dept": form.department.data, "vacc": form.status.data})
            conn.commit()
            flash(f"Student {form.name.data} has been added!", "success")
            return redirect(url_for("student", student_id=form.id.data))
        else:
            flash(f"Student {form.name.data} already exists!", "danger")
        conn.close()
    return render_template("add.html", form=form)


@app.route("/search", methods=["GET", "POST"])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        conn = db_connect()
        c = conn.cursor()
        student = c.execute("SELECT * FROM students WHERE id=:id", {"id": form.id.data}).fetchone()
        if student is not None:
            flash(f"Student with ID: {form.id.data} has been found!", "success")
            return redirect(url_for("student", student_id=form.id.data))
        else:
            flash("No such entry exists!", "danger")
        conn.close()
    return render_template("search.html", form=form)


@app.route("/<int:student_id>")
def student(student_id):
    conn = db_connect()
    c = conn.cursor()
    student = c.execute("SELECT * FROM students WHERE id=:id", {"id": student_id}).fetchone()
    if student is None:
        conn.close()
        abort(404)
    conn.close()
    return render_template("student.html", student=student)


@app.route("/<int:student_id>/update", methods=["GET", "POST"])
def update(student_id):
    conn = db_connect()
    c = conn.cursor()
    student = c.execute("SELECT * FROM students WHERE id=:id", {"id": student_id}).fetchone()
    if student is None:
        conn.close()
        abort(404)
    form = AddForm()
    if form.validate_on_submit():
        c.execute("UPDATE students SET name=:name, id=:id, dept=:dept, vaccine=:vacc WHERE id=:old_id",
                  {"name": form.name.data,
                   "id": form.id.data,
                   "dept": form.department.data,
                   "vacc": form.status.data,
                   "old_id": student_id})
        conn.commit()
        conn.close()
        flash("Student data has been updated!", "success")
        return redirect(url_for("student", student_id=form.id.data))
    elif request.method == 'GET':
        form.name.data = student[0]
        form.id.data = student[1]
        form.department.data = student[2]
        form.status.data = student[3]
    return render_template("update.html", form=form)


@app.route("/remove", methods=["GET", "POST"])
def remove():
    form = RemoveForm()
    if form.validate_on_submit():
        conn = db_connect()
        c = conn.cursor()
        student = c.execute("SELECT * FROM students WHERE id=:id", {"id": form.id.data}).fetchone()
        if student is not None:
            c.execute("DELETE FROM students WHERE id=:id", {"id": form.id.data})
            conn.commit()
            flash(f"Student with ID: {form.id.data} has been removed!", "success")
            return redirect(url_for("home"))
        else:
            flash("No such entry exists!", "danger")
        conn.close()
    return render_template("remove.html", form=form)


@app.route("/stats")
def stats():
    create_plot()
    return render_template("stats.html")


@app.route("/database")
def database():
    conn = db_connect()
    c = conn.cursor()
    students = c.execute("SELECT * FROM students").fetchall()
    conn.close()
    return render_template("database.html", students=students)


if __name__ == "__main__":
    app.run(debug=True)
