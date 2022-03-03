from flask import render_template, url_for, redirect, flash, request
from app import app, db, departments
from app.utils import create_plot
from app.forms import AddForm, SearchForm, RemoveForm
from app.models import Student


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/add", methods=["GET", "POST"])
def add():
    form = AddForm()
    if form.validate_on_submit():
        student = Student(id=form.id.data,
                          name=form.name.data,
                          department=form.department.data,
                          vaccine_status=form.status.data)
        if not student.verify_student():
            db.session.add(student)
            db.session.commit()
            flash(f"Student {form.name.data} has been added!", "success")
            return redirect(url_for("record", student_id=form.id.data))
        else:
            flash(f"Student {form.name.data} already exists!", "danger")
    return render_template("add.html", form=form)


@app.route("/search", methods=["GET", "POST"])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        student = Student.query.get(form.id.data)
        if student is not None:
            flash(f"Student with ID: {form.id.data} has been found!", "success")
            return redirect(url_for("record", student_id=form.id.data))
        else:
            flash("No such entry exists!", "danger")
    return render_template("search.html", form=form)


@app.route("/<int:student_id>")
def record(student_id):
    student = Student.query.get_or_404(student_id)
    return render_template("student.html", student=student, department=departments[student.department - 1])


@app.route("/<int:student_id>/update", methods=["GET", "POST"])
def update(student_id):
    student = Student.query.get_or_404(student_id)
    form = AddForm()
    form.enter.label.text = "Update"
    if form.validate_on_submit():
        student.id = form.id.data
        student.name = form.name.data
        student.department = form.department.data
        student.vaccine_status = form.status.data
        db.session.commit()
        flash("Student data has been updated!", "success")
        return redirect(url_for("record", student_id=form.id.data))
    elif request.method == 'GET':
        form.name.data = student.name
        form.id.data = student.id
        form.department.data = student.department
        form.status.data = student.vaccine_status
    return render_template("update.html", form=form)


@app.route("/remove", methods=["GET", "POST"])
def remove():
    form = RemoveForm()
    if form.validate_on_submit():
        student = Student.query.get(form.id.data)
        if student is not None:
            db.session.delete(student)
            db.session.commit()
            flash(f"Student with ID: {form.id.data} has been removed!", "success")
            return redirect(url_for("home"))
        else:
            flash("No such entry exists!", "danger")
    return render_template("remove.html", form=form)


@app.route("/stats")
def stats():
    create_plot()
    return render_template("stats.html")


@app.route("/database")
def database():
    students = Student.query.all()
    return render_template("database.html", students=students)

