from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    fullname = Column(String(150), nullable=False)


class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    group_name = Column(String(50), nullable=False)


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    fullname = Column(String(150), nullable=False)
    group_id = Column('group_id', ForeignKey('groups.id', ondelete='CASCADE', onupdate='CASCADE'))
    group = relationship('Group', backref='students')


class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    subject_name = Column(String(175), nullable=False)
    teacher_id = Column('teacher_id', ForeignKey('teachers.id', ondelete='CASCADE', onupdate='CASCADE'))
    teacher = relationship('Teacher', backref='subjects')


class Mark(Base):
    __tablename__ = 'marks'
    id = Column(Integer, primary_key=True)
    mark = Column(Integer, nullable=False)
    mark_date = Column('mark_date', Date, nullable=True)
    student_id = Column('student_id', ForeignKey('students.id', ondelete='CASCADE', onupdate='CASCADE'))
    subject_id = Column('subject_id', ForeignKey('subjects.id', ondelete='CASCADE', onupdate='CASCADE'))
    student = relationship('Student', backref='mark')
    subject = relationship('Subject', backref='mark')
