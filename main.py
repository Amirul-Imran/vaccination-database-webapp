from flask import Flask, render_template, url_for, flash, redirect, abort, request
from forms import AddForm, SearchForm, RemoveForm
from utils import db_connect, create_plot


app = Flask(__name__)
app.config["SECRET_KEY"] = "c8b49ab7a60dcb042d7d8148617fdf91"
departments = ['Mechanical', 'Electrical', 'Chemical', 'Civil', 'Biomedical']


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
            c.execute("INSERT INTO students VALUES (:name, :id, :dept, :vacc)",
                      {"name": form.name.data, "id": form.id.data, "dept": form.department.data,
                       "vacc": form.status.data})
            conn.commit()
            flash(f"Student {form.name.data} has been added!", "success")
            conn.close()
            return redirect(url_for("record", student_id=form.id.data))
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
            conn.close()
            return redirect(url_for("record", student_id=form.id.data))
        else:
            flash("No such entry exists!", "danger")
        conn.close()
    return render_template("search.html", form=form)


@app.route("/<int:student_id>")
def record(student_id):
    conn = db_connect()
    c = conn.cursor()
    student = list(c.execute("SELECT * FROM students WHERE id=:id", {"id": student_id}).fetchone())
    if student is None:
        conn.close()
        abort(404)
    student[2] = departments[student[2] - 1]
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
    form.enter.label.text = "Update"
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
        return redirect(url_for("record", student_id=form.id.data))
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
            conn.close()
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
    for index, s in enumerate(students):
        students[index] = list(students[index])
        students[index][2] = departments[students[index][2] - 1]
    conn.close()
    return render_template("database.html", students=students)


if __name__ == "__main__":
    app.run(debug=True)
