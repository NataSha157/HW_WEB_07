from sqlalchemy import func, desc, select, and_, text

from Database.db import session
from Database.models_main import Group, Student, Teacher, Subject, Mark


def select_1():
    """
    SELECT
        s.id,
        s.fullname,
        ROUND(AVG(m.mark), 2) AS average_mark
    FROM students s
    JOIN marks m ON s.id = m.student_id
    GROUP BY s.id
    ORDER BY average_mark DESC
    LIMIT 5;
    """
    res = session.query(Student.id, Student.fullname, func.round(func.avg(Mark.mark), 2).label('average_mark')) \
        .select_from(Student).join(Mark).group_by(Student.id).order_by(desc('average_mark')).limit(5).all()
    return res


def select_2():
    """
    --2.Знайти студента із найвищим середнім балом з певного предмета.
    SELECT
        s.id,
        s.fullname,
        ROUND(AVG(m.mark), 2) AS average_mark
    FROM marks m
    JOIN students s ON s.id = m.student_id
    where m.subject_id = 3
    GROUP BY s.id
    ORDER BY average_mark DESC
    LIMIT 1;
    """
    res = session.query(Student.id, Student.fullname, func.round(func.avg(Mark.mark), 2).label('average_mark')) \
        .select_from(Mark).join(Student).filter(Mark.subject_id == 3) \
        .group_by(Student.id).order_by(desc('average_mark')).limit(1).all()
    return res


def select_3():
    """
    --3.Знайти середній бал у групах з певного предмета.
    SELECT
        s.group_id,
        (SELECT g.group_name
        FROM groups g
        WHERE s.group_id = g.id) AS group_name,
        ROUND(AVG(m.mark), 2) AS average_mark
    FROM marks m
    JOIN students s ON s.id = m.student_id
    WHERE m.subject_id = 7
    GROUP BY s.group_id;
    """
    res = session.query(Student.group_id, func.round(func.avg(Mark.mark), 2).label('average_mark')) \
        .select_from(Mark).join(Student).filter(Mark.subject_id == 7).group_by(Student.group_id).all() # Це мій полегшений варіант
    # res = session.query(Group.group_name, func.round(func.avg(Mark.mark), 2)).select_from(Group).join(Student)\
    #     .join(Mark).filter(Mark.subject_id == 7).group_by(Group.group_name).all() # Це варіант ментора
    return res

def select_4():
    """
    --4.Знайти середній бал на потоці (по всій таблиці оцінок)
    SELECT ROUND(AVG(m.mark), 2) AS average_mark
    from marks m;
    """
    res = session.query(func.round(func.avg(Mark.mark), 2).label('average_mark')).select_from(Mark).first()
    return res

def select_5():
    """
    --5.Знайти які курси читає певний викладач.
    SELECT
        s.subject_name,
        t.fullname
    FROM subjects s
    JOIN teachers t on t.id = s.teacher_id
    WHERE t.id = 2;
    """
    res = session.query(Subject.subject_name, Teacher.fullname).select_from(Subject).join(Teacher).filter(
        Teacher.id == 2).all()
    return res


def select_6():
    """
    --6.Знайти список студентів у певній групі.
    SELECT
        s.id,
        s.fullname,
        g.group_name
    FROM students s
    JOIN groups g ON g.id = s.group_id
    WHERE s.group_id  = 1
    ORDER BY s.id;
    """
    res = session.query(Student.id, Student.fullname, Group.group_name).select_from(Student).join(Group).\
        filter(Student.group_id == 1).all()
    return res


def select_7():
    """
    --7.Знайти оцінки студентів у окремій групі з певного предмета.
    SELECT
        m.mark,
        s.fullname
    FROM marks m
    JOIN students s ON s.id = m.student_id
    WHERE m.subject_id = 3 AND s.group_id = 1
    ORDER BY s.id;
    """
    res = session.query(Mark.mark, Student.fullname).select_from(Mark).join(Student).\
        filter(and_(Mark.subject_id == 3, Student.group_id == 1)).order_by(Student.id).all()
    return res


def select_8():
    """
    --8.Знайти середній бал, який ставить певний викладач зі своїх предметів.
    select
        (SELECT t.fullname FROM teachers t WHERE s.teacher_id = t.id ) AS teacher,
        s.subject_name,
        round(avg(m.mark), 2) as average_mark
    FROM marks m
    JOIN subjects s ON m.subject_id = s.id
    where s.teacher_id = 2
    group by teacher, s.subject_name;
    """
    teacher = session.query(Teacher.fullname.label('teacher')).filter(Teacher.id == 2).subquery()
    sub = session.query(teacher, Subject.subject_name, func.round(func.avg(Mark.mark), 2).label('average_mark'))\
        .select_from(Mark).join(Subject).filter(Subject.teacher_id == 2).group_by(teacher, Subject.subject_name).all()
    return sub


def select_9():
    """
    --9.Знайти список курсів, які відвідує студент.
    SELECT
        s.fullname,
        (SELECT s2.subject_name
        FROM subjects s2
        WHERE m.subject_id = s2.id) AS course
    FROM marks m
    JOIN students s ON m.student_id = s.id
    where s.id = 7
    group by m.subject_id, s.fullname
    order BY course;
    """
    res = session.query(Subject.subject_name).join(Mark).filter(Mark.student_id == 7).group_by(
        Subject.subject_name).all()
    return res



def select_10():
    """
    --10.Список курсів, які певному студенту читає певний викладач.
    SELECT
        s.subject_name
    FROM marks m
    JOIN subjects s ON m.subject_id = s.id
    WHERE m.student_id = 24 and s.teacher_id = 1
    GROUP BY s.subject_name;
    """
    res = session.query(Subject.subject_name).select_from(Mark).join(Subject)\
        .filter(and_(Mark.student_id == 24, Subject.teacher_id == 1)).group_by(Subject.subject_name).all()
    return res

def select_11():
    """
    --11.Середній бал, який певний викладач ставить певному студентові.
    SELECT
        ROUND(AVG(m.mark), 2) AS average_mark
    FROM marks m
    JOIN subjects s ON m.subject_id  = s.id
    WHERE s.teacher_id = 2 AND m.student_id  = 32;
    """
    res = session.query(func.round(func.avg(Mark.mark), 2)).select_from(Mark).join(Subject)\
        .filter(and_(Subject.teacher_id == 2, Mark.student_id == 32)).all()
    return res

def select_12():
    """
    --12.Оцінки студентів у певній групі з певного предмета на останньому занятті.
    select
        s.fullname,
        m.mark,
        m.mark_date
    from marks m
    join students s on m.student_id = s.id
    where m.subject_id = 2 and s.group_id = 3 and m.mark_date = (
        select max(m2.mark_date)
        from marks m2
        join students s2 on s2.id = m2.student_id
        where m2.subject_id = 2 and s2.group_id = 3);
    """
    subquery = session.query(func.max(Mark.mark_date)).select_from(Mark).join(Student)\
        .filter(and_(Mark.subject_id == 2, Student.group_id == 3)).scalar_subquery()
    res = session.query(Student.fullname, Mark.mark, Mark.mark_date).select_from(Mark).join(Student)\
        .filter(and_(Mark.subject_id == 2, Student.group_id == 3, Mark.mark_date == subquery)).one()
    return res
if __name__ == "__main__":
    print(select_1())
    print(select_2())
    print(select_3())
    print(select_4())
    print(select_5())
    print(select_6())
    print(select_7())
    print(select_8())
    print(select_9())
    print(select_10())
    print(select_11())
    print((select_12()))

