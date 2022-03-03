import numpy as np
from app.models import Student
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def create_plot():
    no_shots = [0, 0, 0, 0, 0, 0]
    one_shot = [0, 0, 0, 0, 0, 0]
    two_shots = [0, 0, 0, 0, 0, 0]

    items = Student.query.all()

    for item in items:
        if item.vaccine_status == 0:
            no_shots[item.department] += 1
            no_shots[0] += 1
        elif item.vaccine_status == 1:
            one_shot[item.department] += 1
            one_shot[0] += 1
        else:
            two_shots[item.department] += 1
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
    plt.savefig("app/static/stats.jpg")
    plt.plot()
    plt.clf()
