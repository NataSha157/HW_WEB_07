# Заповнення таблиць
from random import randint
from faker import Faker

from sqlalchemy.exc import SQLAlchemyError

from Database.db import session
from Database.models_main import Group, Student, Teacher, Subject, Mark

NUM_GROPE = 3
NUM_TEACHER = 5
NUM_SUBJECT = 7
NUM_STUDENT = 50
NUM_MARK = 20

res_g = []
res_t = []
res_sj = []
res_st = []
res_m = []

fake = Faker()

if __name__ == '__main__':
    try:
        for _ in range(NUM_GROPE):
            group = Group(group_name=fake.word())
            res_g.append(group)
        session.add_all(res_g)
        for _ in range(NUM_TEACHER):
            teacher = Teacher(fullname=fake.name())
            res_t.append(teacher)
        session.add_all(res_t)
        for _ in range(NUM_SUBJECT):
            subject = Subject(subject_name=fake.word(), teacher_id=randint(1, NUM_TEACHER))
            res_sj.append(subject)
        session.add_all(res_sj)
        for _ in range(NUM_STUDENT):
            student = Student(fullname=fake.name(), group_id=randint(1, NUM_GROPE))
            res_st.append(student)
        session.add_all(res_st)
        for student_id in range(1, NUM_STUDENT + 1):
            for _ in range(NUM_MARK):
                mark = Mark(student_id=student_id, subject_id=randint(1, NUM_SUBJECT), mark=randint(0, 100),
                            mark_date=fake.date_this_decade())
                res_m.append(mark)
        session.add_all(res_m)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        print(e)
    finally:
        session.close()
