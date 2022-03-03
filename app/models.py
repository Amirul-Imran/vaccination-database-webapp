from app import db


class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    name = db.Column(db.Text, nullable=False)
    department = db.Column(db.Integer, nullable=False)
    vaccine_status = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Student('{self.id}', '{self.name}')"

    def verify_student(self):
        student = Student.query.filter_by(id=self.id).first()
        if student:
            return True
        return False
